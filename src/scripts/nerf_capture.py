import numpy as np
import cv2
import carla

from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera, CameraSettings
from src.util.timer import Timer
from src.util.transform_file import TransformFile

def camera_to_world(camera_transform: carla.Transform) -> carla.Transform:
    # Get camera-to-world transformation matrix
    camera_matrix = camera_transform.get_matrix()

    # Apply transformation to camera location
    camera_location = camera_transform.location
    camera_location_hom = np.array([camera_location.x, camera_location.y, camera_location.z, 1.0])
    camera_location_world_hom = np.matmul(camera_matrix, camera_location_hom)
    camera_location_world = carla.Location(x=camera_location_world_hom[0], y=camera_location_world_hom[1], z=camera_location_world_hom[2])

    # Apply transformation to camera rotation
    camera_rotation = camera_transform.rotation
    camera_rotation_hom = np.array([camera_rotation.roll, camera_rotation.pitch, camera_rotation.yaw, 1.0])
    camera_rotation_world_hom = np.matmul(camera_matrix, camera_rotation_hom)
    camera_rotation_world = carla.Rotation(roll=camera_rotation_world_hom[0], pitch=camera_rotation_world_hom[1], yaw=camera_rotation_world_hom[2])

    # Set camera transform in world coordinate frame
    camera_transform_world = carla.Transform(camera_location_world, camera_rotation_world)
    return camera_transform_world


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(0, autopilot=True)
    ego = spawn_ego(autopilot=True)

    # Ignore traffic lights 100% of the time
    session.traffic_manager.ignore_lights_percentage(ego, 100)

    camera_settings = CameraSettings(image_size_x=800, image_size_y=600, fov=90)
    # camera = Camera(parent=ego, transform=carla.Transform(carla.Location(z=2.7), carla.Rotation(pitch=-15)), settings=camera_settings)
    camera = Camera(parent=ego, settings=camera_settings)
    camera_queue = camera.add_numpy_queue()
    camera.start()
    timer_iter = Timer()
    window_title = 'Camera'
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

    # Create a TransformFile
    transform_file = TransformFile()

    # Set the intrinsics of the camera
    transform_file.set_intrinsics(camera_settings.image_size_x, camera_settings.image_size_y, camera_settings.fov)

    image_tick = 0
    ticks_per_image = 3

    while image_tick <= 70 * ticks_per_image:
        timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')

        session.world.tick()
        image = camera_queue.get()

        # Store image every n-th tick
        if image_tick % ticks_per_image == 0:
            # Retrieve image and transformation matrix from camera sensor
            camera_transform_world = camera_to_world(camera.actor.get_transform())

            # Store the image at a given path
            # transform_file.append_frame(image, camera.actor.get_transform()) - OLD
            # transform_file.append_frame(image, camera_transform_world)
            transform_file.append_frame(image, camera.actor.get_transform())

        cv2.imshow(window_title, image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        image_tick += 1

    cv2.destroyWindow(window_title)
    transform_file.export_transforms()