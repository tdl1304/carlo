from dataclasses import dataclass
from typing import Optional

import carla
import numpy as np
import open3d as o3d
import matplotlib

from .sensor import SensorBase


@dataclass
class LidarSettings:
    channels: Optional[int] = None
    range: Optional[float] = None
    points_per_second: Optional[int] = None
    rotation_frequency: Optional[float] = None
    upper_fov: Optional[float] = None
    lower_fov: Optional[float] = None
    horizontal_fov: Optional[float] = None
    atmosphere_attenuation_rate: Optional[float] = None
    dropoff_general_rate: Optional[float] = None
    dropoff_intensity_limit: Optional[float] = None
    dropoff_zero_intensity: Optional[float] = None
    noise_stddev: Optional[float] = None


class Lidar(SensorBase[carla.LidarMeasurement, LidarSettings]):
    DEFAULT_BLUEPRINT = 'sensor.lidar.ray_cast'

    def add_numpy_queue(self):
        """Creates a queue that receives LIDAR data as numpy arrays."""

        def transform(measurement: carla.LidarMeasurement) -> np.ndarray:
            data = np.copy(np.frombuffer(measurement.raw_data, dtype=np.dtype('f4')))
            data = np.reshape(data, (int(data.shape[0] / 4), 4))
            return data

        return self.add_queue(transform=transform)

    def add_pointcloud_queue(self):
        """Creates a queue that receives LIDAR data as Open3D PointClouds."""

        VIRIDIS = np.array(matplotlib.cm.get_cmap('plasma').colors)
        VID_RANGE = np.linspace(0.0, 1.0, VIRIDIS.shape[0])

        def transform(measurement: carla.LidarMeasurement) -> o3d.geometry.PointCloud:
            data = np.copy(np.frombuffer(measurement.raw_data, dtype=np.dtype('f4')))
            data = np.reshape(data, (int(data.shape[0] / 4), 4))

            # Isolate the intensity and compute a color for it
            intensity = data[:, -1]
            intensity_col = 1.0 - np.log(intensity) / np.log(np.exp(-0.004 * 100))
            int_color = np.c_[
                np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 0]),
                np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 1]),
                np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 2])
            ]

            points = data[:, :-1]

            points[:, :1] = -points[:, :1]

            pc = o3d.geometry.PointCloud()
            pc.points = o3d.utility.Vector3dVector(points)
            pc.colors = o3d.utility.Vector3dVector(int_color)
            return pc

        return self.add_queue(transform=transform)
