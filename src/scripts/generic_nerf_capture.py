from dataclasses import dataclass
from typing import List
import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_ego, spawn_vehicles
from src.sensors.camera_rig import CameraRig
from src.util.timer import Timer
from src.util.transform_file import TransformFile

overhead_camera_transform = carla.Transform(carla.Location(z=12.7), carla.Rotation(pitch=-90))


@dataclass
class ExperimentSettings:
    camera_rigs: List[CameraRig]
    ticks_per_image: int = 3
    turns: int = 2
    spawn_transform: carla.Transform = carla.Transform(carla.Location(x=106.386559, y=-2.362594, z=0.5),
                                                       carla.Rotation(pitch=0, yaw=-90, roll=0))


def setup_traffic_manager(traffic_manager: carla.TrafficManager, ego: carla.Actor, turns: int):
    traffic_manager.ignore_lights_percentage(ego, 100)  # Ignore traffic lights 100% of the time
    traffic_manager.set_route(ego, ["Left"] * turns)


def run_session(experiment_settings: List[ExperimentSettings]):

    for experiment in experiment_settings:
        with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
            image_tick = 0
            ticks_per_image = experiment.ticks_per_image
            previous_action = None
            turns = 0
            stop_next_straight = False
            next_action = None

            ego = spawn_ego(autopilot=True, spawn_point=experiment.spawn_transform, filter="vehicle.tesla.model3")
            setup_traffic_manager(session.traffic_manager, ego, experiment.turns)

            for camera_rig in experiment.camera_rigs:
                camera_rig.create_camera(ego)

            timer_iter = Timer()
            window_title = 'Camera'
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

            # Create a TransformFile
            transform_file = TransformFile()

            # Set the intrinsics of the camera
            camera_settings = experiment.camera_rigs[0].get_camera_settings()
            transform_file.set_intrinsics(camera_settings.image_size_x,
                                          camera_settings.image_size_y,
                                          camera_settings.fov)

            while not (next_action == "LaneFollow" and stop_next_straight):
                timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
                session.world.tick()

                # Stack images together horizontally
                image = cv2.hconcat([camera_rig.get_image() for camera_rig in experiment.camera_rigs])

                # Show image
                cv2.imshow(window_title, image)

                # Store image every n-th tick
                if image_tick % ticks_per_image == 0:
                    for camera_rig in experiment.camera_rigs:
                        transform_file.append_frame(camera_rig.previous_image,
                                                    camera_rig.camera.actor.get_transform())

                # Determine if we should stop the next straight
                next_action = session.traffic_manager.get_next_action(ego)[0]
                if (next_action == "Left" and previous_action != "Left"):
                    turns += 1
                    if (turns == experiment.turns):
                        stop_next_straight = True
                previous_action = next_action

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                image_tick += 1

            cv2.destroyWindow(window_title)
            transform_file.export_transforms()


exp_1 = [ExperimentSettings(
    turns=1,
    camera_rigs=[
        CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=-30))),
        CameraRig(transform=overhead_camera_transform),
        CameraRig(transform=carla.Transform(carla.Location(z=3.0), carla.Rotation(yaw=30))),
    ]
)]

run_session(exp_1)
