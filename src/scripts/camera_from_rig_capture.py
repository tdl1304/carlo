import sys
import pathlib

from queue import Queue
from typing import List

import carla
import cv2
import numpy as np

from src.common.rig import Rig, Sensor, parse_rig_json
from src.common.session import Session
from src.common.spawn import spawn_ego, spawn_vehicles
from src.sensors.camera import Camera, CameraSettings
from src.sensors.camera_rig import CameraRig
from src.sensors.lidar import Lidar
from src.util.timer import Timer
from src.util.vehicle import get_back_axle_position

if not len(sys.argv) == 2:
    print(f"Usage: {pathlib.Path(__file__).name} <rig.json>")
    sys.exit(1)

if not pathlib.Path(sys.argv[1]).exists():
    print(f"Rig file {sys.argv[1]} does not exist")
    sys.exit(1)

rig = parse_rig_json(sys.argv[1])
scale = 2


def lidar_to_histogram_features(lidar, yt: float):
    """
    Convert LiDAR point cloud into 2-bin histogram over 256x256 grid
    """
    def splat_points(point_cloud):
        # 256 x 256 grid
        pixels_per_meter = 8
        hist_max_per_pixel = 5
        x_meters_max = 16
        y_meters_max = 32
        xbins = np.linspace(-x_meters_max, x_meters_max, 32*pixels_per_meter+1)
        ybins = np.linspace(-y_meters_max, 0, 32*pixels_per_meter+1)
        hist = np.histogramdd(point_cloud[..., :2], bins=(xbins, ybins))[0]
        hist[hist>hist_max_per_pixel] = hist_max_per_pixel
        overhead_splat = hist/hist_max_per_pixel
        return overhead_splat

    below = lidar[lidar[...,2]<=-yt]
    above = lidar[lidar[...,2]> -yt]
    below_features = splat_points(below)
    above_features = splat_points(above)
    features = np.stack([above_features, below_features], axis=-1)
    features = np.transpose(features, (2, 0, 1)).astype(np.float32)
    features = np.rot90(features, -1, axes=(1,2)).copy()
    return features


def lidar_to_img(lidar, yt):
    lidar[:, 1] *= -1
    img = lidar_to_histogram_features(lidar, yt)
    img = (img * 255).astype(np.uint8)
    img = img.transpose(1, 2, 0)
    img = np.pad(img, ((0, 0), (0, 0), (1, 1)))
    return 255 - img

def make_sensor_transform(sensor: Sensor) -> carla.Transform:
        return carla.Transform(
            carla.Location(
                x=sensor.nominal_sensor_2_rig.x,
                y=-sensor.nominal_sensor_2_rig.y,
                z=sensor.nominal_sensor_2_rig.z,
            ) + sensor_offset,
            carla.Rotation(
                pitch=sensor.nominal_sensor_2_rig.pitch,
                yaw=-sensor.nominal_sensor_2_rig.yaw,
                roll=sensor.nominal_sensor_2_rig.roll,
            ),
        )



with Session() as session:
    # vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True, filter="vehicle.*")
    # ego = spawn_ego(autopilot=True, filter="vehicle.kia.*")
    print(f"Ego: {ego}")

    session.world.tick()

    ego_tf = ego.get_transform()
    back_axle_position = get_back_axle_position(ego)
    back_axle_offset = back_axle_position - ego_tf.location

    sensor_offset = carla.Vector3D(
        x=back_axle_offset.dot(ego_tf.get_forward_vector()),
        y=back_axle_offset.dot(ego_tf.get_right_vector()),
        z=back_axle_offset.dot(ego_tf.get_up_vector()),
    )

    print(f'Ego position: {ego_tf}')
    print(f"Back axle position: {back_axle_position}")
    print(f"Back axle offset: {back_axle_offset}")
    print(f"Sensor offset: {sensor_offset}")

    camera_queues = {}
    #lidar_queues = {}

    cameras = list(filter(lambda sensor: sensor.is_camera, rig.sensors))
    #lidars = {sensor.name: sensor for sensor in rig.sensors if sensor.name == 'lidar:top'}


    
    for sensor in cameras:
        camera_rig = CameraRig(transform=make_sensor_transform(sensor), camera_settings=CameraSettings(
            fov=sensor.fov,
            image_size_x=sensor.properties.width // scale,
            image_size_y=sensor.properties.height // scale,
        ))
        camera_rig.create_camera(ego)

    # for name, sensor in lidars.items():
    #         lidar = Lidar(parent=ego, transform=make_sensor_transform(sensor), settings={

    #         })
    #         lidar_queue = lidar.add_numpy_queue()
    #         lidar.start()
    #         lidar_queues[name] = lidar_queue

    window_title = "Camera"
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    blank = np.zeros((cameras[0].properties.height // scale, cameras[0].properties.width // scale, 4), np.uint8)
    half_blank = np.zeros((cameras[0].properties.height // scale,
                          cameras[0].properties.width // scale // 2, 4), np.uint8)

    while True:
        session.world.tick()
        
        # ! SHOW IMAGES
        # show the front cameras at the top row
        cam_data = {name: camera_queue.get() for name, camera_queue in camera_queues.items()}
        #lidar_data = {name: lidar_queue.get() for name, lidar_queue in lidar_queues.items()}

        # if 'lidar:top' in lidar_data:
        #     lidar_img = lidar_to_img(lidar_data['lidar:top'], make_sensor_transform(lidars['lidar:top']).location.z)
        #     lidar_img = cv2.resize(lidar_img, (cameras[0].properties.width // scale, cameras[0].properties.height // scale))
        # else:
        #     lidar_img = blank

        top_row = [half_blank, cam_data['C1_front60Single'], cam_data['C3_tricam120'], cam_data['C2_tricam60'], half_blank]
        mid_row = [cam_data['C6_L1'], cam_data['C7_L2'], cam_data['C8_R2'], cam_data['C5_R1']]
        bot_row = [blank, half_blank, cam_data['C4_rearCam'], half_blank, blank]

        im_top = np.concatenate(top_row, axis=1)
        im_mid = np.concatenate(mid_row, axis=1)
        im_bot = np.concatenate(bot_row, axis=1)
        im = np.concatenate([im_top, im_mid, im_bot], axis=0)

        cv2.imshow(window_title, im)
        # ! SHOW IMAGES

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyWindow(window_title)
