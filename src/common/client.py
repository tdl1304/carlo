import os
import contextlib

import carla
from .log import info

CARLA_HOST = os.environ.get('CARLA_HOST', 'localhost')
CARLA_PORT = int(os.environ.get('CARLA_PORT', '2000'))

info(f'Connecting to CARLA server at {CARLA_HOST}:{CARLA_PORT}')

client = carla.Client(CARLA_HOST, CARLA_PORT)
world = client.get_world()
blueprints = world.get_blueprint_library()
world_map = world.get_map()
tm = client.get_trafficmanager()

info('Connected.')


def reload_world(reset_settings: bool = False):
    client.reload_world(reset_settings)
    info('Reloaded world.')


@contextlib.contextmanager
def sync_mode(dt: float = 0.1, phys_dt: float = 0.01, phys_substeps: int = 10):
    if not 1 <= phys_substeps <= 16:
        raise ValueError('phys_substeps must be between 1 and 16 inclusive')

    if dt > phys_dt * phys_substeps:
        raise ValueError('dt must be less than or equal to phys_dt * phys_substeps')

    try:
        tm.set_synchronous_mode(True)

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = dt
        settings.substepping = True
        settings.max_substep_delta_time = phys_dt
        settings.max_substeps = phys_substeps
        world.apply_settings(settings)

        info('Enabled synchronous mode.')

        yield

    finally:
        tm.set_synchronous_mode(False)

        settings = world.get_settings()
        settings.synchronous_mode = False
        settings.fixed_delta_seconds = None
        world.apply_settings(settings)

        info('Disabled synchronous mode.')
