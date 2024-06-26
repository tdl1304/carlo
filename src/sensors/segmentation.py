from dataclasses import dataclass
from queue import Queue

import carla
import numpy as np

from src.sensors.camera import CameraSettings
from .sensor import SensorBase

class Segmentation(SensorBase[carla.Image, CameraSettings]):
    DEFAULT_BLUEPRINT = 'sensor.camera.semantic_segmentation'
    
    def add_numpy_queue(self) -> 'Queue[np.ndarray]':
        """Creates a queue that receives camera images as numpy arrays."""

        def transform(image: carla.Image) -> np.ndarray:
            image.convert(carla.ColorConverter.CityScapesPalette)
            data = np.frombuffer(image.raw_data, dtype=np.uint8)
            data = np.reshape(data, (image.height, image.width, 4))
            return data

        return self.add_queue(transform=transform)
    
    def __str__(self) -> str:
        return super().__str__() + f", settings={self.settings}"
