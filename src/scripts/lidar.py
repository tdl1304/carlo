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

freq = 10

with Session(dt=1 / freq, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(filter='vehicle.lincoln.mkz_2020', autopilot=True)

    lidar = Lidar(parent=ego,
                  transform=carla.Transform(carla.Location(z=2.0)),
                  settings=LidarSettings(
                      range=100,
                      noise_stddev=0.1,
                      upper_fov=25,
                      lower_fov=-25,
                      channels=64,
                      rotation_frequency=freq,
                      points_per_second=100000,
                  ))
    lidar_queue = lidar.add_pointcloud_queue()

    camera = Camera(parent=ego,
                    transform=carla.Transform(carla.Location(z=2.0)),
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

    frame = 0
    while True:
        with Timer('iteration: {avg:.3f} s, {fps:.1f} Hz'):
            with Timer('\ttick: {avg:.3f} s, {fps:.1f} Hz'):
                session.world.tick()

            with Timer('\tdata: {avg:.3f} s, {fps:.1f} Hz'):
                camera_data = camera_queue.get()
                lidar_data = lidar_queue.get()

            with Timer('\tgui : {avg:.3f} s, {fps:.1f} Hz'):
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

                cv2.imshow('RGB Camera', camera_data)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        sys.stdout.flush()
    sys.stdout.flush()

    lidar.stop()
    camera.stop()
    
    cv2.destroyAllWindows()
    vis.destroy_window()
