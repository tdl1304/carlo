from datetime import datetime
import json
import os
import sys
from pathlib import Path
import numpy as np

def conversion(matrix: np.ndarray):
    matrix_1 = np.array([[1, 0, 0, 0],
                [0, 0, -1, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 1]])

    # # Step 1: Flip around Z
    # matrix_2 = np.array([[0, 0, 1, 0],
    #                 [0, 1, 0, 0],
    #                 [-1, 0, 0, 0],
    #                 [0, 0, 0, 1]])

    # # Step 1: Flip around Y
    # matrix_3 = np.array([[0, -1, 0, 0],
    #                         [1, 0, 0, 0],
    #                         [0, 0, 1, 0],
    #                         [0, 0, 0, 1]])
    
    # Step 2: Multiply the transformation matrix with the conversion matrix
    transformed_matrix = np.matmul(matrix_1, matrix)
    # transformed_matrix = np.matmul(matrix_2, transformed_matrix)
    # transformed_matrix = np.matmul(matrix_3, transformed_matrix)
    
    # # Step 3: Flip the y and z coordinates of the resulting matrix
    # transformed_matrix[0] = -transformed_matrix[0]
    # transformed_matrix[1] = -transformed_matrix[1]
    
    # Convert the numpy array to a list of lists and return the resulting matrix
    return transformed_matrix.tolist()

def convert(file_prefix: str = None):
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
            'transform_matrix': new_transform
        }
        new_frames.append(new_frame)
    
    # Overwrite frames
    new_transforms['frames'] = new_frames

    # Create archive file-path
    dt = datetime.now()
    timestamp = int(datetime.timestamp(dt))
    file_prefix = file_prefix or timestamp
    archive_path = run_path / "archive" / f'{file_prefix}_transforms.json'
    
    # Save new transforms to archive
    with open(archive_path, 'w+') as f:
        json.dump(new_transforms, f, indent=4)
    
    # Overwrite old transforms
    with open(run_path / "transforms.json", 'w+') as f:
        json.dump(new_transforms, f, indent=4)
        print(f"\nSuccessfully overwrote transforms.json")
    print(f"\nNew transforms saved to {archive_path}")

if __name__ == "__main__":
    file_prefix = None
    if len(sys.argv) > 1:
        file_prefix = sys.argv[1:][0]
    convert(file_prefix)