import os
from pathlib import Path

import numpy as np
import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_ego
from src.experiments import experiments
from src.experiments.experiment_settings import Experiment
from src.util.confirm_overwrite import confirm_path_overwrite
from src.util.create_slurm_script import create_slurm_script
from src.util.timer import Timer
from src.util.transform_file import TransformFile


def setup_traffic_manager(traffic_manager: carla.TrafficManager, ego: carla.Actor, turns: int):
    traffic_manager.ignore_lights_percentage(ego, 100)  # Ignore traffic lights 100% of the time
    traffic_manager.set_route(ego, ["Left"] * turns)


def get_distance_traveled(prev_location, current_location):
    print(f"prev_location: {prev_location}")
    print(f"current_location: {current_location}")
    return np.sqrt((current_location.x - prev_location.x)**2 + (current_location.y - prev_location.y)**2 + (current_location.z - prev_location.z)**2)


# Stops if number of turns is reached or if distance traveled is greater than stop_distance
def should_stop(next_action, stop_next_straight, distance_traveled, stop_distance):
    if next_action == "LaneFollow" and stop_next_straight:
        return True

    if distance_traveled >= stop_distance:
        return True

    return False



def run_session(experiment: Experiment):

    # Create directory for experiment
    root_path = Path(os.curdir)
    experiment_path = root_path / "runs" / experiment.experiment_name
    os.makedirs(experiment_path, exist_ok=True)

    # Save the experiment settings to the experiment directory
    settings_path = experiment_path / "experiment_settings.txt"
    confirm_path_overwrite(settings_path)
    with open(settings_path, "w") as f:
        f.write(str(experiment))
        print(f"✅ Saved experiment settings to {experiment_path / 'experiment_settings.txt'}")

    # Create a slurm script for the experiment
    create_slurm_script(carlo_data_dir=experiment_path,
                        input_data_dir=f"../carlo/{experiment_path}", output_dir=f"../carlo/{experiment_path}", experiment_name=experiment.experiment_name)

    with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:

        # Run all the experiments in the same session.
        for index, run in enumerate(experiment.experiments):
            ego = spawn_ego(autopilot=True, spawn_point=run.spawn_transform, filter="vehicle.tesla.model3")
            setup_traffic_manager(session.traffic_manager, ego, run.turns)

            image_tick = 0
            ticks_per_image = run.ticks_per_image
            previous_action = None
            turns = 0
            stop_next_straight = False
            next_action = None
            distance_traveled = 0
            prev_location = run.spawn_transform.location

            for camera_rig in run.camera_rigs:
                camera_rig.create_camera(ego)

            timer_iter = Timer()
            window_title = 'Camera'
            cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

            # Create a TransformFile
            transform_file = TransformFile(output_dir=experiment_path / str(index))

            # Set the intrinsics of the camera
            camera_settings = run.camera_rigs[0].get_camera_settings()
            transform_file.set_intrinsics(camera_settings.image_size_x,
                                          camera_settings.image_size_y,
                                          camera_settings.fov)

            while not (should_stop(next_action, stop_next_straight, distance_traveled, run.stop_distance)):
                # timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
                session.world.tick()

                # Stack images together horizontally
                image = cv2.hconcat([camera_rig.get_image() for camera_rig in run.camera_rigs])

                # Show image
                cv2.imshow(window_title, image)

                # Store image and update distance traveled every n-th tick.
                if image_tick % ticks_per_image == 0:
                    for camera_rig in run.camera_rigs:
                        transform_file.append_frame(camera_rig.previous_image,
                                                    camera_rig.camera.actor.get_transform())

                    current_location = ego.get_location()
                    distance_traveled += get_distance_traveled(prev_location, current_location)
                    prev_location = current_location
                    print(f"Total distance traveled: {distance_traveled:.2f} meters")

                # Determine if we should stop the next straight
                next_action = session.traffic_manager.get_next_action(ego)[0]
                if (next_action == "Left" and previous_action != "Left"):
                    turns += 1
                    if (turns == run.turns):
                        stop_next_straight = True
                previous_action = next_action

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                image_tick += 1

            print("\n\nNEXT EXPERIMENT\n\n")
            transform_file.export_transforms()

        cv2.destroyWindow(window_title)


experiment = experiments.experiment_6
run_session(experiment)
