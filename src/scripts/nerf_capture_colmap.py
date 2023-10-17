import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera, CameraSettings
from src.util.carla_to_nerf import carla_to_nerf
from src.util.timer import Timer
from src.util.transform_file import TransformFile

with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(0, autopilot=True)
    ego = spawn_ego(autopilot=True)
    image_tick = 0
    ticks_per_image = 3

    # Ignore traffic lights 100% of the time
    session.traffic_manager.ignore_lights_percentage(ego, 100)

    camera_settings = CameraSettings(image_size_x=400, image_size_y=300, fov=90)
    # camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15)), settings=camera_settings)
    # camera_queue = camera.add_numpy_queue()

    camera_right = Camera(parent=ego, transform=carla.Transform(
        carla.Location(z=2.7), carla.Rotation(yaw=30)), settings=camera_settings)
    camera_right_queue = camera_right.add_numpy_queue()

    camera_left = Camera(parent=ego, transform=carla.Transform(carla.Location(
        z=2.7), carla.Rotation(yaw=-30)), settings=camera_settings)
    camera_left_queue = camera_left.add_numpy_queue()

    # camera.start()
    camera_right.start()
    camera_left.start()

    timer_iter = Timer()
    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    # Create a TransformFile
    transform_file = TransformFile()

    # Set the intrinsics of the camera
    transform_file.set_intrinsics(camera_settings.image_size_x, camera_settings.image_size_y, camera_settings.fov)

    camera = Camera(parent=ego, )
    camera_queue = camera.add_numpy_queue()

    while image_tick <= 70 * ticks_per_image:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')

        session.world.tick()

        # image = camera_queue.get()
        image_left = camera_left_queue.get()
        image_right = camera_right_queue.get()

        # Stack images together horizontally
        image = cv2.hconcat([image_left, image_right])

        # Store image every n-th tick
        if image_tick % ticks_per_image == 0:
            transform_file.append_frame(image_left, camera_left.actor.get_transform())
            transform_file.append_frame(image_right, camera_right.actor.get_transform())

        cv2.imshow(window_title, image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        image_tick += 1

    print("Destroying actors")
    session.destroy_actors([ego]+vehicles)
    cv2.destroyWindow(window_title)
    transform_file.export_transforms()
