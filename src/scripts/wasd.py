import cv2
import sys
import glob
import os

# ==============================================================================
# -- Find CARLA module ---------------------------------------------------------
# ==============================================================================
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- Add PythonAPI for release mode --------------------------------------------
# ==============================================================================
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass

import carla
from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer

print("Staring WASD script")
with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    print("Session started")  
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=False)
    
    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15)))
    camera_queue = camera.add_numpy_queue()
    
    camera_back = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15, yaw=180)))
    camera_back_queue = camera_back.add_numpy_queue()
    
    camera.start()
    camera_back.start()

    timer_iter = Timer()

    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    throttle = 0.0
    steer = 0.0
    reverse = 0.0

    while True:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')

        session.world.tick()
        image = camera_queue.get()
        image_back = camera_back_queue.get()
        print(camera.actor.get_transform())
        
        image = cv2.hconcat([image, image_back])
        cv2.imshow(window_title, image)

        key = cv2.waitKey(1) & 0xFF

        throttle *= 0.9
        steer *= 0.9
        reverse *= 0.9

        if key == ord('w'):
            throttle = 1.0
        if key == ord('s'):
            throttle = 1.0
            reverse = 1.0
        if key == ord('a'):
            steer = -1.0
        if key == ord('d'):
            steer = 1.0
        control = carla.VehicleControl(throttle=throttle, steer=steer, reverse=reverse > 0.5)
        ego.apply_control(control)

        if key == ord('q'):
            break
    
    cv2.destroyWindow(window_title)
