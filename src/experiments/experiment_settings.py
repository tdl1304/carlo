from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import carla

from src.sensors.camera_rig import CameraRig


@dataclass
class ExperimentSettings:
    camera_rigs: List[CameraRig]
    ticks_per_image: int = 3
    turns: int = 3 # Equivalent to one lap around the block
    stop_distance: int = 100
    spawn_transform: carla.Transform = carla.Transform(carla.Location(x=106.386559, y=-2.362594, z=0.5),
                                                       carla.Rotation(pitch=0, yaw=-90, roll=0))

@dataclass
class Experiment:
    experiments: List[ExperimentSettings]
    experiment_name: str = field(default_factory=lambda: str(int(datetime.timestamp(datetime.now()))))