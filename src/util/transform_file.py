import json
import os
from pathlib import Path
import carla
import cv2

from numpy import ndarray
from datetime import datetime

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
            self.output_dir = root_path / str(int(datetime.timestamp(dt)))
        
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.image_dir = self.output_dir / 'images'
        self.image_dir.mkdir(exist_ok=True, parents=True)

    def append_frame(self, image: ndarray, transform: carla.Transform):
        # Save the image to output
        file_path = str(self.image_dir / f'{self.count:04d}.png')
        cv2.imwrite(file_path, image)
        self.count += 1

        # Get the matrix from the transform
        transform_matrix = transform.get_matrix()

        self.frames.append({
            'file_path': file_path,
            'transform': transform_matrix
        })
    
    def set_intrinsics(self, intrinsics):
        self.intrinsics = intrinsics

    def export_transforms(self, file_path='transforms.json'):
        output_path = self.output_dir / file_path
        with open(output_path, 'w+') as f:
            obj = {
                'intrinsics': self.intrinsics,
                'frames': self.frames
            }
            json.dump(obj, f, indent=4)