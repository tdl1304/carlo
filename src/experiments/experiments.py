from dataclasses import dataclass
from typing import List
from src.experiments.experiment_settings import Experiment, ExperimentSettings
from src.sensors.camera_rig import CameraRig
import carla

overhead_camera_transform = carla.Transform(carla.Location(z=12.7), carla.Rotation(pitch=-90))

# Create a comment-block saying "EXPERIMENT 1"

##############################################
# Experiment 1: 2 cameras, yaw at 10, 30, 50, 70, 90 degrees
##############################################


experiment_1 = [
    ExperimentSettings(
        turns=3,
        camera_rigs=[
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-10))),
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=10))),
        ]
    ),
    ExperimentSettings(
        turns=3,
        camera_rigs=[
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
        ]
    ),
    ExperimentSettings(
        turns=3,
        camera_rigs=[
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-50))),
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=50))),
        ]
    ),
    ExperimentSettings(
        turns=3,
        camera_rigs=[
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-70))),
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=70))),
        ]
    ),
    ExperimentSettings(
        turns=3,
        camera_rigs=[
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-90))),
            CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=90))),
        ]
    ),
]

##############################################
# Experiment 2: Capacity - how many turns? how many meters?
##############################################

experiment_2 = Experiment(
    experiments=[
        ExperimentSettings(
            stop_distance=50,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-60))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=0))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=60))),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-60))),
                # CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=0))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=60))),
            ]
        ),
    ],
    experiment_name='exp_capacity_1'
)
