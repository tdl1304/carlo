import dataclasses
from queue import Queue
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

import carla

from src.common.session import session


_T = TypeVar('_T')
_S = TypeVar('_S')
_O = TypeVar('_O')


class Sensor(Generic[_T]):
    """Represents a Carla Sensor.
    
    Provides convenience methods for spawning sensors and retrieving data from them.
    """

    _callbacks: List[Callable[[_T], None]]
    actor: carla.Sensor

    def __init__(self, actor: carla.Sensor) -> None:
        super().__init__()
        self._callbacks = []
        self.actor = actor

    def add_callback(self, callback: Callable[[_T], None]) -> None:
        """Adds a callback that is called when new sensor data is received."""
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[_T], None]) -> None:
        """Removes a callback."""
        self._callbacks.remove(callback)

    def add_queue(self, transform: Callable[[_T], _O] = lambda x: x) -> 'Queue[_O]':
        """Creates a queue that receives (optionally transformed) sensor data.
        
        :transform: A function that transforms the sensor data before it is put into the queue.
        """
        queue = Queue()

        def writer(x):
            return queue.put(transform(x))

        # Store the queue on the writer callback so we can find it later during removal.
        writer._queue = queue

        self.add_callback(writer)
        return queue

    def remove_queue(self, queue: Queue) -> None:
        """Removes a queue."""
        for callback in self._callbacks:
            if getattr(callback, '_queue', None) is queue:
                self.remove_callback(callback)
                break
        else:
            raise ValueError('queue not found')

    def start(self) -> None:
        """Starts listening for sensor data."""
        self.actor.listen(self._put)

    def stop(self) -> None:
        """Stops listening for sensor data."""
        self.actor.stop()
    
    def destroy(self) -> None:
        """Destroys the sensor."""
        self.actor.destroy()

    def _put(self, value: _T) -> None:
        for callback in self._callbacks:
            callback(value)


class SensorBase(Sensor[_T], Generic[_T, _S]):
    """Base class for new Carla sensor wrapper types.

    Subclasses should define their own sensor settings dataclass,
    and pass the sensor data type and settings type as type parameters
    when inheriting from this class.

    Subclasses should define a DEFAULT_BLUEPRINT class attribute that
    specifies the default blueprint to use for the sensor.
    """

    DEFAULT_BLUEPRINT: Optional[str] = None

    def __init__(self, *,
                 actor: Optional[carla.Sensor] = None,
                 settings: Union[None, _S, Dict[str, Any]] = None,
                 blueprint: Union[None, str, carla.ActorBlueprint] = None,
                 transform: Optional[carla.Transform] = None,
                 parent: Optional[carla.Actor] = None,
                 attachment_type: carla.AttachmentType = carla.AttachmentType.Rigid,
                 ) -> None:

        if actor is None:
            actor = self._make_actor(
                blueprint=blueprint,
                transform=transform,
                parent=parent,
                attachment_type=attachment_type,
                settings=settings,
            )
            
        super().__init__(actor)


    @classmethod
    def _make_actor(cls, *,
                    blueprint: Union[None, str, carla.ActorBlueprint] = None,
                    transform: Optional[carla.Transform] = None,
                    parent: Optional[carla.Actor] = None,
                    attachment_type: carla.AttachmentType = carla.AttachmentType.Rigid,
                    settings: Union[None, _S, Dict[str, Any]] = None,
                    ) -> carla.Sensor:
        if blueprint is None:
            blueprint = cls.DEFAULT_BLUEPRINT

        if blueprint is None:
            raise ValueError(f'blueprint must be specified ({cls.__name__}.DEFAULT_BLUEPRINT is missing)')

        if isinstance(blueprint, str):
            blueprint = session.blueprints.find(blueprint)

        if transform is None:
            transform = carla.Transform()

        if settings is not None:
            if dataclasses.is_dataclass(settings):
                settings = dataclasses.asdict(settings)
            if isinstance(settings, dict):
                for key, value in settings.items():
                    if value is not None:
                        print('setting', key, value)
                        blueprint.set_attribute(key, str(value))  # type: ignore
            else:
                raise TypeError('settings must be a dataclass or dict')

        return session.world.spawn_actor(
            blueprint,
            transform,
            attach_to=parent,
            attachment_type=attachment_type
        )
