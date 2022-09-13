import carla

from .session import session
from .log import info


def add_camera(
    sensor_type: str = 'sensor.camera.rgb',
    transform: carla.Transform = carla.Transform(carla.Location(z=2)),
    parent: carla.Actor = None,
):
    """Add a camera to the world."""
    blueprint = session.blueprints.find(sensor_type)
    camera = session.world.spawn_actor(blueprint, transform, attach_to=parent)
    info(f'Added {sensor_type}')
    return camera
