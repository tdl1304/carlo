import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7)))
    camera_queue = camera.add_numpy_queue()
    
    camera.start()

    timer_iter = Timer()

    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    while True:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
        session.world.tick()
        image = camera_queue.get()
        cv2.imshow(window_title, image)
        
        transform = camera.actor.get_transform()
        print(f"Location: {transform.location}")
        print(f"Rotation: {transform.rotation}")
        print(f"Transform matrix: {transform.get_matrix()}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyWindow(window_title)
