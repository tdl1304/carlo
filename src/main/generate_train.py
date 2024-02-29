import argparse
import os
import pathlib

import carla
import cv2
from datetime import datetime

import numpy as np

from src.common.session import Session
from src.common.spawn import spawn_ego, spawn_vehicles
from src.sensors.camera import Camera
from src.util.timer import Timer



parser = argparse.ArgumentParser(
                    prog='python -m src.main.generate_train_set',
                    description='Generates images from carla',
                    epilog='Enjoy the program! :)')
parser.add_argument('-gen-images', dest="generate_images", help='Generate images or not', default=False, action="store_true")
parser.add_argument('-headless', help='Run in headless mode or not', default=False, action="store_true")
args = parser.parse_args()

generate_images = args.generate_images
headless = args.headless

print("args"+str(args))

downscaleFactor = 3
baseResX = 1920
baseResY = 1208
fov = 90


with Session() as session:
    #vehicles = spawn_vehicles(1, autopilot=True)
    session.traffic_manager.global_percentage_speed_difference(50)
    ego = spawn_ego(autopilot=True, filter="vehicle.*")
    session.traffic_manager.vehicle_lane_offset(ego, 0)
    session.traffic_manager.ignore_lights_percentage(ego, 100)
    print(f"Ego: {ego}")

    camLeft = {"image_size_x": baseResX//downscaleFactor, 
               "image_size_y": baseResY//downscaleFactor, 
               "fov": fov, 
               "transform": carla.Transform(carla.Location(z=2.7), carla.Rotation(yaw=-10)), 
               "name": "C_Left"}
    camRight = {"image_size_x": baseResX//downscaleFactor,
                "image_size_y": baseResY//downscaleFactor, 
                "fov": fov, 
                "transform": carla.Transform(carla.Location(z=2.7), carla.Rotation(yaw=10)), 
                "name": "C_Right"}
    
    cameras = [camLeft, camRight]
    camera_queues = {}

    for sensor in cameras:
        camera = Camera(parent=ego, transform=sensor["transform"], settings={
                        "fov": sensor["fov"],
                        "image_size_x": sensor["image_size_x"],
                        "image_size_y": sensor["image_size_y"]
                        })   
        camera_queue = camera.add_numpy_queue()
        camera.start()
        camera_queues[sensor["name"]] = camera_queue

    timer_iter = Timer()

    # Create a window to show the camera
    if not headless:
        window_title = "Camera"
        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
    
    # Create a directory to store the images
    if generate_images:
        root_path = pathlib.Path(os.curdir)
        output_dir = root_path / "runs" / str(int(datetime.timestamp(datetime.now())))
        output_dir.mkdir(exist_ok=True, parents=True)

    # settings and initial values
    image_tick = 0
    ticks_per_image = 5
    count = 0
    skip_ticks = 25
    while image_tick <= 70 * ticks_per_image + skip_ticks:
        timer_iter.tick("dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz")
        session.world.tick()

        # show the front cameras at the top row
        cam_data = {name: camera_queue.get() for name, camera_queue in camera_queues.items()}
       
        if not headless:
            row = [cam_data['C_Left'], cam_data['C_Right']]
            im = np.concatenate(row, axis=1)
            cv2.imshow(window_title, im)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Store image every n-th tick
        if generate_images and image_tick > skip_ticks and image_tick % ticks_per_image == 0 :
            # Store the image at a given path
            for name in cam_data.keys():
                image = cam_data[name]
                file_path = str(output_dir/ f'{name}_{count:04d}.png')
                cv2.imwrite(file_path, image)
            count += 1
        image_tick += 1

    if not headless:
        cv2.destroyWindow(window_title)
    session.destroy_actors([ego])

