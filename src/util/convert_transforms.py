from datetime import datetime
import json
import os
from pathlib import Path
import numpy as np

def conversion(matrix: np.ndarray):
    conversion_matrix = np.array([[1, 0, 0, 0],
                        [0, 0, -1, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]])
    new_matrix = np.matmul(conversion_matrix, matrix)
    return new_matrix

def convert():
    root_path = Path(os.curdir)
    run_path = root_path / 'runs/no_conversion_run'
    transforms_path = run_path / 'transforms.json'
    frames = None

    with open(transforms_path, 'r') as f:
        transforms = json.load(f)
        frames = transforms['frames']

    new_frames = []
    for frame in frames:
        
        new_transform = conversion(frame['transform_matrix'])
        new_frame = {
            'file_path': frame['file_path'],
            'transform_matrix': new_transform.tolist()
        }
        new_frames.append(new_frame)
    

    # Create new file-path
    dt = datetime.now()
    new_file_path = run_path / f'{int(datetime.timestamp(dt))}_transforms.json'

    # Save new transforms
    with open(new_file_path, 'w+') as f:
        transforms['frames'] = new_frames
        json.dump(transforms, f, indent=4)

    print(f"\nNew transforms saved to {new_file_path}")

if __name__ == "__main__":
    convert()