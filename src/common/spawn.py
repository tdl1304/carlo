import random
from typing import List

import carla

from .session import session
from .log import info


def spawn_vehicles(
    count: int,
    filter: str = 'vehicle.*',
    retries: int = 10,
    autopilot: bool = False
) -> List[carla.Vehicle]:
    """Spawn vehicles at random spawn points."""
    actors: List[carla.Vehicle] = []
    spawn_points = session.map.get_spawn_points()
    while len(actors) < count:
        spawn_point = random.choice(spawn_points)
        blueprint = random.choice(session.blueprints.filter(filter))
        actor = session.world.try_spawn_actor(blueprint, spawn_point)
        if actor:
            actors.append(actor)
            if autopilot:
                actor.set_autopilot(True)
        else:
            if retries == 0:
                break
            retries -= 1
    info(f'Spawned {len(actors)} vehicles')
    return actors


def spawn_ego(
    filter: str = 'vehicle.*',
    autopilot: bool = False
) -> carla.Vehicle:
    """Spawn ego vehicle at random spawn point."""
    ego, = spawn_vehicles(1, filter, retries=-1, autopilot=autopilot)
    return ego
