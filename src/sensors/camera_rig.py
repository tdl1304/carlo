from numpy import ndarray
from src.sensors.camera import Camera, CameraSettings
import carla


class CameraRig:
    base_camera_settings = CameraSettings(image_size_x=600, image_size_y=450, fov=90)
    base_rotation = carla.Rotation(yaw=0, pitch=0, roll=0)
    base_location = carla.Location(z=3.0)
    base_transform = carla.Transform(base_location, base_rotation)

    def __init__(self, transform: carla.Transform = base_transform, camera_settings: CameraSettings = base_camera_settings):
        self.transform = transform
        self.camera_settings = camera_settings
        self.camera = None
        self.camera_queue = None
        self.previous_image = None

    def create_camera(self, parent: carla.Actor) -> Camera:
        self.camera = Camera(parent=parent, transform=self.transform, settings=self.camera_settings)
        self.camera_queue = self.camera.add_numpy_queue()
        self.camera.start()

    def get_camera_settings(self) -> CameraSettings:
        return self.camera_settings

    def get_camera(self, parent: carla.Actor) -> Camera:
        return Camera(parent=parent, transform=self.transform, settings=self.camera_settings)

    def get_image(self) -> ndarray:
        image = self.camera_queue.get()
        self.previous_image = image
        return image

    def __str__(self) -> str:
        return f"CameraRig(transform={self.transform}, camera_settings={self.camera_settings})"
    
    def __repr__(self) -> str:
        return self.__str__()
