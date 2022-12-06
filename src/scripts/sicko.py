import random
from queue import Queue

import numpy as np
import cv2

import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera, CameraSettings
from src.util.stopwatch import Stopwatch
from src.util.ema import ExponentialMovingAverage
from src.util.timer import Timer

control_state = {
    'prev': carla.VehicleControl(),
}

def get_control() -> carla.VehicleControl:
    prev = control_state['prev']

    if prev.throttle > 0.1 and random.random() < 0.8:
        return prev

    throttle = prev.throttle
    steer = prev.steer
    brake = prev.brake
    reverse = prev.reverse

    if random.random() < 0.1:
        throttle = random.random()
    elif random.random() < 0.5:
        throttle = min(1, max(0, throttle + random.uniform(-0.1, 0.2)))

    if random.random() < 0.1:
        steer = random.uniform(-1, 1)
    elif random.random() < 0.5:
        steer = min(1, max(-1, steer + random.uniform(-0.1, 0.1)))
    
    if not brake and random.random() < 0.01:
        brake = 1
        throttle = 0
    elif brake and random.random() < 0.1:
        brake = 0
        throttle = random.uniform(0.2, 1)

    if reverse and random.random() < 0.2:
        reverse = False
    if not reverse and random.random() < 0.1:
        reverse = True

    control = carla.VehicleControl(
        throttle=throttle,
        steer=steer,
        brake=brake,
        reverse=reverse,
    )
    control_state['prev'] = control
    return control


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=False)

    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.0)), settings=CameraSettings())
    camera_queue = camera.add_numpy_queue()

    timer_iter = Timer()

    camera.start()

    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    while True:
        timer_iter.tick('iter: {avg:.3f} s, FPS: {fps:.1f} Hz')

        control = get_control()
        ego.apply_control(control)

        session.world.tick()
        image = camera_queue.get()

        cv2.imshow(window_title, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(window_title)
