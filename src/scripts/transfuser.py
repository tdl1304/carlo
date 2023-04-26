import sys
import time
import numpy as np

import carla
import cv2
import open3d as o3d

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.lidar import Lidar, LidarSettings
from src.sensors.camera import Camera, CameraSettings
from src.util.timer import Timer


def add_open3d_axis(vis):
    """Add a small 3D axis on Open3D Visualizer"""
    axis = o3d.geometry.LineSet()
    axis.points = o3d.utility.Vector3dVector(np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]]))
    axis.lines = o3d.utility.Vector2iVector(np.array([
        [0, 1],
        [0, 2],
        [0, 3]]))
    axis.colors = o3d.utility.Vector3dVector(np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]]))
    vis.add_geometry(axis)


def lidar_to_histogram_features(lidar):
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

    below = lidar[lidar[...,2]<=-2.3]
    above = lidar[lidar[...,2]>-2.3]
    below_features = splat_points(below)
    above_features = splat_points(above)
    features = np.stack([above_features, below_features], axis=-1)
    features = np.transpose(features, (2, 0, 1)).astype(np.float32)
    features = np.rot90(features, -1, axes=(1,2)).copy()
    return features

with Session(dt=1 / 20, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(filter='vehicle.lincoln.mkz_2020', autopilot=True)

    lidar = Lidar(parent=ego,
                transform=carla.Transform(
                    carla.Location(x=1.3, y=0, z=2.4),
                    carla.Rotation(yaw=-90)),
                settings=LidarSettings(
                    range=85,
                    rotation_frequency=10,
                    points_per_second=600000,
                    #   rotation_frequency=20,
                    #   points_per_second=1200000,
                    channels=64,
                    upper_fov=10,
                    lower_fov=-30,
                    atmosphere_attenuation_rate=0.004,
                    dropoff_general_rate=0.45,
                    dropoff_intensity_limit=0.8,
                    dropoff_zero_intensity=0.4,
                ))
    lidar_queue = lidar.add_pointcloud_queue()
    lidar_np_queue = lidar.add_numpy_queue()

    camera = Camera(parent=ego,
                    transform=carla.Transform(
                        carla.Location(x=1.3, y=0, z=2.3),
                        carla.Rotation(yaw=0)),
                    settings=CameraSettings(
                        image_size_x=320,
                        image_size_y=160,
                        fov=60)
                    )
    camera_queue = camera.add_numpy_queue()

    lidar.start()
    camera.start()

    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name='Carla Lidar',
        width=960,
        height=540,
        left=480,
        top=270)
    vis.get_render_option().background_color = [0.05, 0.05, 0.05]
    vis.get_render_option().point_size = 1
    vis.get_render_option().show_coordinate_frame = True
    add_open3d_axis(vis)

    point_list = o3d.geometry.PointCloud()

    # Enable stdout buffering so we can flush once per iteration.
    sys.stdout = open(1, 'w', buffering=1024)

    timer_iter = Timer()
    timer_tick = Timer()
    timer_data = Timer()
    timer_gui = Timer()

    frame = 0
    while True:
        with timer_tick.ctx('\ttick: {avg:.3f} s, {fps:.1f} Hz'):
            session.world.tick()

        with timer_data.ctx('\tdata: {avg:.3f} s, {fps:.1f} Hz'):
            camera_data = camera_queue.get()
            lidar_data = lidar_queue.get()
            lidar_np = lidar_np_queue.get()

        with timer_gui.ctx('\tgui : {avg:.3f} s, {fps:.1f} Hz'):
            point_list.points = lidar_data.points
            point_list.colors = lidar_data.colors

            if frame == 2:
                vis.add_geometry(point_list)
            vis.update_geometry(point_list)

            vis.poll_events()
            vis.update_renderer()
            # # This can fix Open3D jittering issues:
            time.sleep(0.005)
            frame += 1

            lidar_np[:, 1] *= -1
            lidar_img = lidar_to_histogram_features(lidar_np).transpose(1, 2, 0)
            lidar_img = np.pad(lidar_img, ((0, 0), (0, 0), (0, 1)))
            cv2.imshow('Lidar Image', lidar_img)

            cv2.imshow('RGB Camera', camera_data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        timer_iter.tick('iteration: {avg:.3f} s, {fps:.1f} Hz')
        sys.stdout.flush()

    sys.stdout.flush()

    lidar.stop()
    camera.stop()
    
    cv2.destroyAllWindows()
    vis.destroy_window()
