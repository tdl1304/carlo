from src.common.session import Session
from src.common.spawn import spawn_vehicles, spawn_ego
from src.sensors.camera import Camera
from src.util.timer import Timer


with Session(dt=0.1, phys_dt=0.01, phys_substeps=10) as session:
    vehicles = spawn_vehicles(50, autopilot=True)
    ego = spawn_ego(autopilot=True)

    camera = Camera(parent=ego)
    camera_queue = camera.add_queue()
    camera.start()

    while True:
        with Timer('tick    : {avg:.3f} s, FPS: {fps:.1f} Hz'):
            with Timer('  world : {avg:.3f} s, FPS: {fps:.1f} Hz'):
                session.world.tick()
            with Timer('  camera: {avg:.3f} s, FPS: {fps:.1f} Hz'):
                camera_queue.get()
