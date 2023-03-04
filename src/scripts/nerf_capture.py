import math
import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera, CameraSettings
from src.util.timer import Timer
from src.util.transform_file import TransformFile


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(0, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera_settings = CameraSettings(image_size_x=800, image_size_y=600, fov=90)
    camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15)), settings=camera_settings)
    camera_queue = camera.add_numpy_queue()
    camera.start()
    timer_iter = Timer()
    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
    

    # Create a TransformFile
    transform_file = TransformFile()

    # Set the intrinsics of the camera
    transform_file.set_intrinsics(camera_settings.image_size_x, camera_settings.image_size_y, camera_settings.fov)


    while True:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')

        session.world.tick()
        image = camera_queue.get()

        # Store the image at a given path
        transform_file.append_frame(image, camera.actor.get_transform())

        cv2.imshow(window_title, image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyWindow(window_title)
    transform_file.export_transforms()
