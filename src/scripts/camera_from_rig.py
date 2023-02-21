from queue import Queue
from typing import List

import carla
import cv2

from src.common.rig import parse_rig_json
from src.common.session import Session
from src.common.spawn import spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer
from src.util.vehicle import get_back_axle_position

with Session() as session:
    # vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True, filter="vehicle.tesla.model3")

    session.world.tick()

    back_axle_position = get_back_axle_position(ego)

    x_relative_offset = ego.get_transform().location.distance_2d(back_axle_position)
    z_relative_offset = ego.get_transform().location.z - back_axle_position.z

    rig = parse_rig_json("/home/vcxr12/aasewold/carlo/rig_ocam.json")

    sensors = sorted(
        list(filter(lambda sensor: sensor.is_camera, rig.sensors)),
        key=lambda sensor: sensor.nominal_sensor_2_rig.y,
    )

    front_camera_queues: List[Queue] = []
    back_camera_queues: List[Queue] = []

    for sensor in sensors:
        transform = carla.Transform(
            carla.Location(
                x=sensor.nominal_sensor_2_rig.x - x_relative_offset,
                y=sensor.nominal_sensor_2_rig.y,
                z=sensor.nominal_sensor_2_rig.z - z_relative_offset,
            ),
            carla.Rotation(
                pitch=sensor.nominal_sensor_2_rig.pitch,
                yaw=sensor.nominal_sensor_2_rig.yaw,
                roll=sensor.nominal_sensor_2_rig.roll,
            ),
        )

        camera = Camera(parent=ego, transform=transform, settings={"fov": sensor.fov})
        camera_queue = camera.add_numpy_queue()
        camera.start()

        if sensor.is_rear:
            back_camera_queues.append(camera_queue)
        else:
            front_camera_queues.append(camera_queue)

    timer_iter = Timer()

    window_title = "Camera"
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    while True:
        timer_iter.tick("dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz")
        session.world.tick()

        # show the front cameras at the top row
        front_images = [camera_queue.get() for camera_queue in front_camera_queues]
        front_image = cv2.hconcat(front_images)

        cv2.imshow(window_title, front_image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyWindow(window_title)
