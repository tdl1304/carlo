from queue import Queue
from src.common.session import Session
from src.common.sensors import add_camera
from src.common.spawn import spawn_vehicles, spawn_ego
from src.util.timer import Timer


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = add_camera(parent=ego)
    camera_queue = Queue()

    def camera_put(_):
        camera_queue.put(None)

    camera.listen(camera_put)

    while True:
        with Timer('tick    : {avg:.3f} s, FPS: {fps:.1f} Hz'):
            with Timer('  world : {avg:.3f} s, FPS: {fps:.1f} Hz'):
                session.world.tick()
            with Timer('  camera: {avg:.3f} s, FPS: {fps:.1f} Hz'):
                camera_queue.get()
