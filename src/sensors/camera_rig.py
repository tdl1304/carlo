import numpy as np
from src.sensors.camera import Camera, CameraSettings
import carla
from queue import Queue
from src.sensors.depth import Depth

from src.util.carla_to_nerf import carla_to_nerf_3


class CameraRig:
    base_camera_settings = CameraSettings(image_size_x=600, image_size_y=450, fov=90)
    base_rotation = carla.Rotation(yaw=0, pitch=0, roll=0)
    base_location = carla.Location(z=3.0)
    base_transform = carla.Transform(base_location, base_rotation)

    # Constructor
    # transform: carla.Transform(base_location: carla.Location, base_rotation: carla.Rotation)
    def __init__(self, transform: carla.Transform = base_transform, camera_settings: CameraSettings = base_camera_settings):
        self.transform = transform
        self.camera_settings = camera_settings
        self.camera = None
        self.camera_queue = None
        self.previous_image = None

    def create_camera(self, parent: carla.Actor) -> 'CameraRig':
        if self.camera_settings.type == "depth":
            self.camera = Depth(parent=parent, transform=self.transform, settings=self.camera_settings)
        else:
            self.camera = Camera(parent=parent, transform=self.transform, settings=self.camera_settings)
        self.camera_queue = self.camera.add_numpy_queue()
        self.camera.start()
        return self
    
    def get_projection_matrix(self) -> np.ndarray:
        # Get camera settings
        camera_settings = self.get_camera_settings()

        # Intrinsic parameters
        fx = camera_settings.image_size_x / (2.0 * np.tan(np.deg2rad(camera_settings.fov / 2.0)))
        fy = camera_settings.image_size_y / (2.0 * np.tan(np.deg2rad(camera_settings.fov / 2.0)))
        cx = camera_settings.image_size_x / 2.0
        cy = camera_settings.image_size_y / 2.0

        # Intrinsic matrix
        K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ])

        # Extrinsic parameters
        extrinsic_matrix = np.eye(4)  # Assuming no extrinsic transformation for now
        
        translation = np.array([self.transform.location.x, self.transform.location.y, self.transform.location.z])
        rotation = np.deg2rad(np.array([self.transform.rotation.roll, self.transform.rotation.pitch, self.transform.rotation.yaw]))
        
        # TODO transform to desired coordinate system
        #t = carla_to_nerf_3(self.transform)
        rotation_matrix = carla.Transform(np.identity(3))
        rotation_matrix = carla.Transform.rotation_matrix(rotation_matrix, carla.Rotation(yaw=rotation[2], pitch=rotation[1], roll=rotation[0]))

        # Construct the extrinsic matrix
        extrinsic_matrix = np.eye(4)
        extrinsic_matrix[:3, :3] = rotation_matrix
        extrinsic_matrix[:3, 3] = translation

        # KITTI-style projection matrix [3x4]
        projection_matrix = np.dot(K, extrinsic_matrix)[:3, :]  # Discard the last row

        return projection_matrix


    def get_camera_settings(self) -> CameraSettings:
        return self.camera_settings

    def get_camera(self) -> Camera:
        if self.camera is None:
            raise Exception("Camera not created yet")
        return self.camera
    
    def get_camera_queue(self) -> 'Queue[np.ndarray]':
        if self.camera_queue is None:
            raise Exception("Camera not created yet")
        return self.camera_queue

    def get_image(self) -> np.ndarray:
        image = self.camera_queue.get()
        self.previous_image = image
        return image

    def __str__(self) -> str:
        return f"CameraRig(transform={self.transform}, camera_settings={self.camera_settings})"
    
    def __repr__(self) -> str:
        return self.__str__()
