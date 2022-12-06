import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import IO

import carla
import cv2
import typer

from src.common.session import Session
from src.sensors.camera import Camera
from src.util.timer import Timer


def main(
    fpv_img: bool = False,
    bev_img: bool = False,
    fpv_video: bool = True,
    bev_video: bool = True,
    headless: bool = True,
):
    save_dir = Path('.') / 'output' / 'spectate' / datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    fpv_writers = []
    bev_writers = []
    
    if not headless:
        fpv_writers.append(CVWindow('fpv'))
        bev_writers.append(CVWindow('bev'))

    if fpv_img:
        fpv_dir = save_dir / 'fpv'
        fpv_dir.mkdir(parents=True, exist_ok=False)
        fpv_writers.append(ImageSaver(fpv_dir, 'fpv_{:04d}.jpg'))
    if bev_img:
        bev_dir = save_dir / 'bev'
        bev_dir.mkdir(parents=True, exist_ok=False)
        bev_writers.append(ImageSaver(bev_dir, 'bev_{:04d}.jpg'))

    if fpv_video:
        save_dir.mkdir(parents=True, exist_ok=True)
        fpv_writers.append(VideoSaver(save_dir / 'fpv.mp4'))
    if bev_video:
        save_dir.mkdir(parents=True, exist_ok=True)
        bev_writers.append(VideoSaver(save_dir / 'bev.mp4'))

    try:
        with Session(spectate=True) as session:
            for _ in range(3):
                actors = session.world.get_actors().filter('vehicle.*')
                heros = [actor
                        for actor in actors
                        if actor.attributes.get('role_name') == 'hero']
                if len(heros) == 0:
                    time.sleep(1)
                    continue
                elif len(heros) == 1:
                    hero, = heros
                    break
                else:
                    raise RuntimeError('Multiple heros found.')
            else:
                print('No hero vehicle found.')
                sys.exit(1)

            print('Hero:', hero)

            fpv_camera = Camera(parent=hero, transform=carla.Transform(carla.Location(z=3)), settings={'role_name': 'spectate-fpv'})
            bev_camera = Camera(parent=hero, transform=carla.Transform(carla.Location(z=50), carla.Rotation(pitch=-90)), settings={'role_name': 'spectate-bev'})
            fpv_queue = fpv_camera.add_numpy_queue()
            bev_queue = bev_camera.add_numpy_queue()
            fpv_camera.start()
            bev_camera.start()

            timer_iter = Timer()

            try:
                while True:
                    timer_iter.tick('dt: {dt:.3f} s, avg: {avg:.3f} s, FPS: {fps:.1f} Hz')
                    fpv_image = fpv_queue.get()
                    bev_image = bev_queue.get()

                    for writer in fpv_writers:
                        writer(fpv_image)
                    for writer in bev_writers:
                        writer(bev_image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
            finally:
                fpv_camera.destroy()
                bev_camera.destroy()
        
    finally:
        for writer in fpv_writers:
            writer.close()
        for writer in bev_writers:
            writer.close()


class CVWindow:
    def __init__(self, title: str):
        self.title = title
        cv2.namedWindow(self.title, cv2.WINDOW_AUTOSIZE)

    def __call__(self, image):
        cv2.imshow(self.title, image)
    
    def close(self):
        cv2.destroyWindow(self.title)


class ImageSaver:
    def __init__(self, path: Path, filename_format: str):
        self.path = path
        self.filename_format = filename_format
        self.frame = 0
    
    def __call__(self, image):
        img_path = self.path / self.filename_format.format(self.frame)
        cv2.imwrite(str(img_path), image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        self.frame += 1
    
    def close(self):
        pass


class VideoSaver:
    _pipe: IO[bytes]

    def __init__(self, path: Path) -> None:
        # Open an ffmpeg subprocess to save input images as a video
        ffmpeg_args = (
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'warning',
            '-f', 'image2pipe',
            '-vcodec', 'png',
            '-r', '60',
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '18',
            '-frag_duration', str(int(1e6)),
            str(path),
        )
        self._ffmpeg = subprocess.Popen(ffmpeg_args, stdin=subprocess.PIPE)
        self._pipe = self._ffmpeg.stdin  # type: ignore

    def __call__(self, image):
        is_success, buffer = cv2.imencode('.png', image)
        if not is_success:
            print('Failed to encode image.')
        else:
            self._pipe.write(buffer.tobytes())

    def close(self):
        self._pipe.close()
        self._ffmpeg.wait()


if __name__ == '__main__':
    typer.run(main)
