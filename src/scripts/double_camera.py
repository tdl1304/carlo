import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15)))
    camera_queue = camera.add_numpy_queue()
    
    camera_back = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15, yaw=180)))
    camera_back_queue = camera_back.add_numpy_queue()
    
    camera.start()
    camera_back.start()

    timer_iter = Timer()

    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    while True:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')

        session.world.tick()
        image = camera_queue.get()
        image_back = camera_back_queue.get()
        print(camera.actor.get_transform())
        
        # stack images together horiontally
        image = cv2.hconcat([image, image_back])
        cv2.imshow(window_title, image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyWindow(window_title)
