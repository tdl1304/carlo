import os
from typing import Tuple, cast
import random
import sys
import time
import carla
from . import log

class Session:
    _server: Tuple[str, int]
    _dt: float
    _phys_dt: float
    _phys_substeps: int
    _seed: int
    _spectate: bool

    client: carla.Client
    world: carla.World
    blueprints: carla.BlueprintLibrary
    map: carla.Map
    traffic_manager: carla.TrafficManager

    def __init__(self, server: Tuple[str, int] = (None, None), *, dt: float = 0.1, phys_dt: float = 0.01, phys_substeps: int = 10, seed: int = 0, spectate: bool = False):
        self._server = server
        self._dt = dt
        self._phys_dt = phys_dt
        self._phys_substeps = phys_substeps
        self._seed = seed
        self._spectate = spectate
    
    def reload_world(self, reset_settings: bool = False):
        """Reloads the current world.
        
        :param reset_settings: Whether to reset the world settings to their default values.
        For example, this will disable synchronous mode.
        """
        self.world = self.client.reload_world(reset_settings)
        log.info('Reloaded world.')

    def __enter__(self) -> 'Session':
        """Starts the session and sets the global active session."""
        if session._active is not None:
            raise RuntimeError('Session already active')

        try:
            self._connect()

            if self._seed is not None:
                self._set_seed()

            if not self._spectate:
                self._setup_world()

            log.info('Session active.')
            session._active = self
        except Exception as e:
            log.err(f'Failed to start the session: {str(e)}')

        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Stops the session and clears the global active session."""
        if exc_type is None:
            log.info('Exiting session.')
        else:
            log.err(f'Exiting session due to exception:\n\t{exc_type.__name__}: {exc_value}')

        if not self._spectate:
            self._teardown_world()
        
        log.info('Bye!')
        session._active = None  # type: ignore

        if exc_type is KeyboardInterrupt:
            sys.exit(0)

        self.client = None  # Close the client gracefully

    def _connect(self):
        server_host = self._server[0] or os.environ.get('CARLA_HOST', '127.0.0.1')
        server_port = self._server[1] or int(os.environ.get('CARLA_PORT', '2000'))
        server_traffic_manager_port = int(os.environ.get('CARLA_TM_PORT', '8000'))

        log.info(f'Starting session with {server_host}:{server_port}.')

        self.client = carla.Client(server_host, server_port)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.blueprints = self.world.get_blueprint_library()
        self.traffic_manager = self.client.get_trafficmanager(server_traffic_manager_port)
    
    def _set_seed(self):
        log.info('Setting random seed.')
        random.seed(self._seed)
        self.traffic_manager.set_random_device_seed(self._seed)
    
    def _setup_world(self):
        log.info('Applying world settings.')

        self.traffic_manager.set_synchronous_mode(True)

        settings = self.world.get_settings()
        settings.no_rendering_mode = False
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = self._dt
        settings.substepping = True
        settings.max_substep_delta_time = self._phys_dt
        settings.max_substeps = self._phys_substeps
        self.world.apply_settings(settings)
        #self.reload_world(False)
    
    def _teardown_world(self):
        log.info('Cleaning up world.')

        #self.reload_world(True)
        
        settings = self.world.get_settings()
        settings.synchronous_mode = False
        settings.no_rendering_mode = False
        settings.fixed_delta_seconds = None
        self.world.apply_settings(settings)
        self.traffic_manager.set_synchronous_mode(False)
        time.sleep(0.5)

class _SessionProxy:
    """Helper class to allow "reassignment" of the active session
    after the `session` variable has been imported by other modules.
    """
    _active: Session = None  # type: ignore

    def __getattr__(self, key: str):
        return getattr(self._active, key)

session: Session = cast(Session, _SessionProxy())
