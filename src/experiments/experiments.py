from dataclasses import dataclass
from typing import List
from src.experiments.experiment_settings import Experiment, ExperimentSettings
from src.sensors.camera import CameraSettings
from src.sensors.camera_rig import CameraRig
import carla

overhead_camera_transform = carla.Transform(carla.Location(z=12.7), carla.Rotation(pitch=-90))

# Create a comment-block saying "EXPERIMENT 1"

##############################################
# Experiment 1: Camera-setup
##############################################


experiment_1 = Experiment(
    experiment_name='exp_camera_setup_1',
    experiments=[
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-10))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=10))),
            ]
        ),
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-50))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=50))),
            ]
        ),
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-70))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=70))),
            ]
        ),
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-50))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=0))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=50))),
            ]
        ),
        ExperimentSettings(
            stop_distance=125,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-70))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=0))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=70))),
            ]
        ),
    ]
)

##############################################
# Experiment 2: Capacity - how many turns? how many meters?
##############################################

experiment_2 = Experiment(
    experiments=[
        ExperimentSettings(
            stop_distance=50,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            stop_distance=200,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            stop_distance=400,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            stop_distance=800,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
        ExperimentSettings(
            turns=3,
            stop_distance=5000,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),

    ],
    experiment_name='exp_capacity_1'
)

##############################################
# Experiment 3: Test
##############################################

experiment_3 = Experiment(
    experiments=[
        ExperimentSettings(
            stop_distance=50,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-60))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=60))),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-60))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=60))),
            ]
        ),
    ],
    experiment_name='exp_test'
)

##############################################
# Experiment 4: Camera settings
##############################################

camera_settings = [
    CameraSettings(image_size_x=200, image_size_y=150, fov=90),
    CameraSettings(image_size_x=400, image_size_y=300, fov=90),
    CameraSettings(image_size_x=800, image_size_y=600, fov=90),
    CameraSettings(image_size_x=1200, image_size_y=900, fov=90),
    CameraSettings(image_size_x=1600, image_size_y=1200, fov=90),
]

experiment_4 = Experiment(
    experiments=[
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=-30)), camera_settings=camera_settings[0]),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=30)), camera_settings=camera_settings[0]),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=-30)),  camera_settings=camera_settings[1]),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=30)),  camera_settings=camera_settings[1]),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=-30)),  camera_settings=camera_settings[2]),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=30)),  camera_settings=camera_settings[2]),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=-30)),  camera_settings=camera_settings[3]),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=30)),  camera_settings=camera_settings[3]),
            ]
        ),
        ExperimentSettings(
            stop_distance=100,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=-30)),  camera_settings=camera_settings[4]),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0),
                                                    carla.Rotation(yaw=30)),  camera_settings=camera_settings[4]),
            ]
        ),
    ],
    experiment_name='exp_image_size'
)

##############################################
# Experiment 5: Can COLMAP handle a full lap? ⛔

# WITH VOCAB-TREE
# COLMAP only found poses for 4.37% of the images. This is low.
# This can be caused by a variety of reasons, such poor scene coverage, blurry images, or large exposure changes.

# WITH SEQUENTIAL MATCHING
# COLMAP found poses for all images, CONGRATS!

# "fl_x": 199.95200841392978,
# "fl_y": 180.0158372186924,
# "cx": 199.86080786048282,
# "cy": 150.04495224409698,
# "w": 400,
# "h": 300,
# "camera_model": "OPENCV",
# "k1": -0.00031343408304528145,
# "k2": -0.0005933858192653826,
# "p1": -0.00012972942324782972,
# "p2": -0.00021240782388856521,


# THE GENERATED TRANSFORMS.JSON'S INTERNAL PARAMETERS
# "fl_x": 123.47392475671101,
# "fl_y": 92.60544356753326,
# "cx": 200.0,
# "cy": 150.0,
# "w": 400,
# "h": 300,
# "k1": 0,
# "k2": 0,
# "p1": 0,
# "p2": 0,
##############################################

experiment_5 = Experiment(
    experiment_name="exp_full_lap",
    experiments=[
        ExperimentSettings(
            stop_distance=2000,
            turns=3,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
    ],
)

##############################################
# Experiment 6: Can COLMAP handle two full laps?
##############################################

experiment_6 = Experiment(
    experiment_name="exp_two_full_laps",
    experiments=[
        ExperimentSettings(
            stop_distance=2000,
            turns=6,
            camera_rigs=[
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
                CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
            ]
        ),
    ],
)
