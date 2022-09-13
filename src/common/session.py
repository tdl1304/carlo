import os
import sys
from typing import Optional, Tuple, cast

import carla

from .log import info


__all__ = ['session', 'Session']


class Session:
    _server: Tuple[str, int]
    _dt: float
    _phys_dt: float
    _phys_substeps: int

    client: carla.Client
    world: carla.World
    blueprints: carla.BlueprintLibrary
    map: carla.Map
    traffic_manager: carla.TrafficManager

    def __init__(self,
        server: Tuple[str, int] = (None, None),
        *,
        dt: float = 0.1,
        phys_dt: float = 0.01,
        phys_substeps: int = 10,
        seed: Optional[int] = 0,
    ):
        self._server = server
        self._dt = dt
        self._phys_dt = phys_dt
        self._phys_substeps = phys_substeps
        self._seed = seed
    
    def reload_world(self, reset_settings: bool = False):
        self.world = self.client.reload_world(reset_settings)
        info('Reloaded world.')

    def __enter__(self) -> 'Session':
        if session._active is not None:
            raise RuntimeError('Session already active')

        self._connect()

        if self._seed is not None:
            self._set_seed()

        self._setup_world()

        info('Session active.')
        session._active = self
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        info('Exiting session.')
        self.reload_world(True)
        session._active = None
        info('Bye!')

        if exc_type is KeyboardInterrupt:
            sys.exit(0)

    def _connect(self):
        server_host = self._server[0] or os.environ.get('CARLA_HOST', 'localhost')
        server_port = self._server[1] or int(os.environ.get('CARLA_PORT', '2000'))

        info(f'Starting session with {server_host}:{server_port}.')

        self.client = carla.Client(server_host, server_port)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.blueprints = self.world.get_blueprint_library()
        self.traffic_manager = self.client.get_trafficmanager()
    
    def _set_seed(self):
        info('Setting random seed.')

        import random
        random.seed(self._seed)

        import numpy.random
        numpy.random.seed(self._seed)

        self.traffic_manager.set_random_device_seed(self._seed)
    
    def _setup_world(self):
        info('Applying world settings.')

        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = self._dt
        settings.substepping = True
        settings.max_substep_delta_time = self._phys_dt
        settings.max_substeps = self._phys_substeps
        self.world.apply_settings(settings)

        self.reload_world(False)


class _SessionProxy:
    _active: Session = None

    def __getattr__(self, key: str):
        return getattr(self._active, key)


session: Session = cast(Session, _SessionProxy())
