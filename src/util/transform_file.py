import json
import carla
from datetime import datetime

class TransformFile:
    def __init__(self, output_dir=None) -> None:
        self.frames = []
        self.intrinsics = {}
        self.count = 0
        
        if output_dir is not None:
            self.output_dir = output_dir
        else:
            dt = datetime.now()
            self.output_dir = str(int(datetime.timestamp(dt)))
        
        self.image_dir = self.output_dir + '/images'

    def append_frame(self, image: carla.Image, transform: carla.Transform):
        # Save the image to output
        file_path = self.image_dir + '/' + f'{str(self.count):04d}' + '.png'
        image.save_to_disk(file_path)
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
        output_path = self.output_dir + '/' + file_path
        with open(output_path, 'w+') as f:
            obj = {
                'intrinsics': self.intrinsics,
                'frames': self.frames
            }
            json.dump(obj, f, indent=4)