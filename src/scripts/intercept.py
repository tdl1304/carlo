import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List

import cv2
import typer

from src.common.session import Session
from src.sensors.camera import Camera
from src.util.timer import Timer
from src.scripts.spectate import CVWindow, ImageSaver, VideoSaver


def angle_diff(a: float, b: float) -> float:
    """Returns the difference between two angles in degrees."""
    diff = ((a - b) + 180) % 360 - 180
    return 60 * round(diff / 60)


def sort_cameras(cameras: List):
    """Sorts the cameras by their yaw angle."""
    yaws = [camera.get_transform().rotation.yaw for camera in cameras]
    diff_rows = [
        [angle_diff(a, b) for b in yaws]
        for a in yaws
    ]

    for i, row in enumerate(diff_rows):
        if sum(row) == 0:
            break
    else:
        raise ValueError('Could not find middle camera.')

    i_middle = i
    i_left = row.index(60)
    i_right = row.index(-60)

    return cameras[i_left], cameras[i_middle], cameras[i_right]


def main(
    stacked_img: bool = False,
    stacked_video: bool = False,
    headless: bool = True,
):
    save_dir = Path('.') / 'output' / 'intercept' / datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    writers = []
    
    if not headless:
        writers.append(CVWindow('Stacked'))

    if stacked_img:
        stacked_dir = save_dir / 'stacked'
        stacked_dir.mkdir(parents=True, exist_ok=False)
        writers.append(ImageSaver(stacked_dir, 'stacked_{:04d}.jpg'))

    if stacked_video:
        save_dir.mkdir(parents=True, exist_ok=True)
        writers.append(VideoSaver(save_dir / 'stacked.mp4'))

    try:
        with Session(spectate=True) as session:
            for _ in range(3):
                cameras = session.world.get_actors().filter('sensor.camera.rgb')
                cameras = [camera
                            for camera in cameras
                            if camera.attributes.get('role_name') == 'front'
                            and camera.parent.attributes.get('role_name') == 'hero']
                if len(cameras) == 0:
                    time.sleep(1)
                    continue
                elif len(cameras) == 3:
                    break
                else:
                    raise RuntimeError(f'Unexpected number of cameras found ({len(cameras)}).')
            else:
                print('No cameras found.')
                sys.exit(1)

            for camera in cameras:
                print(camera.id, camera.get_transform().rotation)
            cameras = sort_cameras(cameras)

            cameras = [Camera(actor=camera) for camera in cameras]
            queues = [camera.add_numpy_queue() for camera in cameras]
            for camera in cameras:
                camera.start()

            timer_iter = Timer()

            while True:
                timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
                images = [queue.get() for queue in queues]
                stacked = cv2.hconcat(images)

                for writer in writers:
                    writer(stacked)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
    finally:
        for writer in writers:
            writer.close()


if __name__ == '__main__':
    typer.run(main)
