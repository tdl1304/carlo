from dataclasses import dataclass
from queue import Queue
from typing import Optional

import carla
import numpy as np

from .sensor import SensorBase


@dataclass
class CameraSettings:
    fov: Optional[float] = None
    fstop: Optional[float] = None
    image_size_x: Optional[int] = None
    image_size_y: Optional[int] = None
    iso: Optional[float] = None
    gamma: Optional[float] = None
    shutter_speed: Optional[float] = None


class Camera(SensorBase[carla.Image, CameraSettings]):
    DEFAULT_BLUEPRINT = 'sensor.camera.rgb'
    
    def add_numpy_queue(self) -> 'Queue[np.ndarray]':
        """Creates a queue that receives camera images as numpy arrays."""

        def transform(image: carla.Image) -> None:
            data = np.frombuffer(image.raw_data, dtype=np.uint8)
            data = np.reshape(data, (image.height, image.width, 4))
            return data

        return self.add_queue(transform=transform)
