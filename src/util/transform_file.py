import json
import math
import os
from pathlib import Path
import carla
import cv2
import numpy as np

from datetime import datetime

from src.util.transformation_matrix_conversion import unreal_axis_2_blender_conversion, unreal_axis_2_blender_conversion_v2, unreal_axis_2_blender_conversion_v3, unreal_axis_2_blender_conversion_v4

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

        # Get the matrix from the transform
        # transform_matrix = unreal_axis_2_blender_conversion_v4(transform.get_matrix())
        transform_matrix = transform.get_matrix()

        self.frames.append({
            'file_path': f'images/{file_path.split("/")[-1]}',
            'transform_matrix': transform_matrix
        })




    def compute_intrinsics(self, image_size_x, image_size_y, fov):
        computed_fov = math.tan(fov / 2)
        # Potensielt image_size_x / 2, ev. bruk cx, cy
        return {
            "fl_x": image_size_x / computed_fov,
            "fl_y": image_size_y / computed_fov,
            "cx": image_size_x / 2,
            "cy": image_size_y / 2,
            "w": image_size_x,
            "h": image_size_y,
            "camera_model": "OPENCV",
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