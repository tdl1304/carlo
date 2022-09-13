from queue import Queue

import numpy as np
import cv2

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.common.sensors import add_camera
from src.util.stopwatch import Stopwatch
from src.util.ema import ExponentialMovingAverage


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = add_camera(parent=ego)
    camera_queue = Queue()

    timer = Stopwatch()
    frame_time = ExponentialMovingAverage(mixing=0.2, initial=1)

    def camera_put(image):
        data = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))
        camera_queue.put(data)

        dt = timer.elapsed_seconds
        frame_time.update(dt)
        timer.restart()
        print(f'dt: {dt:.3f} s, avg: {frame_time.value:.3f} s, FPS: {1 / frame_time.value:.1f} Hz')
    
    def camera_get():
        session.world.tick()
        return camera_queue.get()

    camera.listen(camera_put)

    def loop():
        window_title = 'Camera'
        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
        while True:
            image = camera_get()
            cv2.imshow(window_title, image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow(window_title)
    
    loop()
