import json
import math
import os
from pathlib import Path
import cv2
import carla
import numpy as np

from datetime import datetime

from src.util.carla_to_nerf import carla_to_nerf_3


class TransformFile:
    def __init__(self, output_dir=None) -> None:
        self.frames = []
        self.intrinsics = {}
        self.count = 0

        root_path = Path(os.curdir)
        if output_dir is not None:
            self.output_dir = root_path / output_dir
        else:
            dt = datetime.now()
            self.output_dir = root_path / "runs" / str(int(datetime.timestamp(dt)))

        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.image_dir = self.output_dir / 'images'
        self.image_dir.mkdir(exist_ok=True, parents=True)

    def append_frame(self, image: np.ndarray, transform: carla.Transform):

        # Save the image to output
        file_path = str(self.image_dir / f'{self.count:04d}.png')
        cv2.imwrite(file_path, image)
        self.count += 1

        self.frames.append({
            'file_path': f'images/{file_path.split("/")[-1]}',
            'transform_matrix': carla_to_nerf_3(transform)
        })

    def compute_intrinsics(self, image_size_x, image_size_y, fov):
        # Intrinsics from COLMAP
        # "fl_x": 199.79105529556688,
        # "fl_y": 81.64220292214017,
        # "cx": 199.7199843662804,
        # "cy": 149.99511991974333,
        # "w": 400,
        # "h": 300,
        # "camera_model": "OPENCV",
        # "k1": -0.0008745578413395661,
        # "k2": -0.00012159146577227206,
        # "p1": 0.00010041156063693768,
        # "p2": -0.0007499095300458892,

        # The FOV is the horizontal FOV. Should equal 1 if fov is 90
        computed_focal_length = math.tan(math.radians(fov / 2))
        fl_x = (0.5 * image_size_x) / computed_focal_length
        fl_y = (0.5 * image_size_y) / computed_focal_length
        return {
            "camera_model": "OPENCV",
            "fl_x": fl_x,
            "fl_y": fl_y,
            "cx": image_size_x / 2,
            "cy": image_size_y / 2,
            "w": image_size_x,
            "h": image_size_y,
            "k1": 0,
            "k2": 0,
            "p1": 0,
            "p2": 0,
        }

    def set_intrinsics(self, image_size_x, image_size_y, fov):
        intrinsics = self.compute_intrinsics(image_size_x=image_size_x, image_size_y=image_size_y, fov=fov)
        self.intrinsics = intrinsics

    def export_transforms(self, file_path='transforms.json'):
        output_path = self.output_dir / file_path
        with open(output_path, 'w+') as f:
            obj = {
                **self.intrinsics,
                'frames': self.frames
            }
            json.dump(obj, f, indent=4)
        print(f"Saved run to {output_path}")
