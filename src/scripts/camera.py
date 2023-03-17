import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_ego
from src.sensors.camera import Camera, CameraSettings
from src.util.timer import Timer


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    spawn_location = carla.Location(x=106.386559, y=-2.362594, z=0.05)
    spawn_rotation = carla.Rotation(pitch=0.000458, yaw=-89.304840, roll=0.017129)
    spawn_transform = carla.Transform(spawn_location, spawn_rotation)

    previous_action = None
    turns = 0
    stop_next_straight = False

    ego = spawn_ego(autopilot=True, spawn_point=spawn_transform)

    session.traffic_manager.ignore_lights_percentage(ego, 100)
    session.traffic_manager.set_route(ego, ["Left", "Left", "Left", "Left"])

    camera_settings = CameraSettings(image_size_x=400, image_size_y=300, fov=90)
    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7)), settings=camera_settings)
    camera_queue = camera.add_numpy_queue()
    camera.start()
    timer_iter = Timer()
    window_title = 'Camera'

    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    while True:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
        session.world.tick()
        image = camera_queue.get()
        cv2.imshow(window_title, image)

        transform = camera.actor.get_transform()
        # session.traffic_manager.force_lane_change(ego, 0)  # 0 = left, 1 = right

        print(f"Next action: {session.traffic_manager.get_next_action(ego)[0]}")
        print(f"Turns: {turns}")

        next_action = session.traffic_manager.get_next_action(ego)[0]
        if (next_action == "Left" and previous_action != "Left"):
            turns += 1

            if (turns == 3):
                stop_next_straight = True

        previous_action = next_action

        if (next_action == "LaneFollow" and stop_next_straight):
            print("Did 4 turns, stopping")
            transform = ego.get_transform()
            location = transform.location
            rotation = transform.rotation
            print(f"Location: {location}")
            print(f"Rotation: {rotation}")
            break

        current_waypoint_id = session.traffic_manager.get_next_action(ego)[1].id

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(window_title)
