from datetime import datetime
import json
import os
from pathlib import Path
import numpy as np

def conversion(matrix: np.ndarray):
    conversion_matrix = np.array([[5, 0, 0, 0],
                        [0, 0, -2, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]])
    new_matrix = np.matmul(conversion_matrix, matrix)
    return new_matrix

def convert():
    root_path = Path(os.curdir)
    run_path = root_path / 'runs/no_conversion_run'
    transforms_path = run_path / 'original_transforms.json'
    
    # Variables for 
    frames = None
    new_transforms = None
    new_frames = []

    with open(transforms_path, 'r') as f:
        new_transforms = json.load(f)
        frames = new_transforms['frames']

    # Convert each frame with the conversion matrix
    for frame in frames:
        new_transform = conversion(frame['transform_matrix'])
        new_frame = {
            'file_path': frame['file_path'],
            'transform_matrix': new_transform.tolist()
        }
        new_frames.append(new_frame)
    
    # Overwrite frames
    new_transforms['frames'] = new_frames

    # Create archive file-path
    dt = datetime.now()
    archive_path = run_path / "archive" / f'{int(datetime.timestamp(dt))}_transforms.json'
    
    # Save new transforms to archive
    with open(archive_path, 'w+') as f:
        json.dump(new_transforms, f, indent=4)
    
    # Overwrite old transforms
    with open(run_path / "transforms.json", 'w+') as f:
        json.dump(new_transforms, f, indent=4)
        print(f"\nSuccessfully overwrote transforms.json")
    print(f"\nNew transforms saved to {archive_path}")

if __name__ == "__main__":
    convert()