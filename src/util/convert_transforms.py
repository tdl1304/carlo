from datetime import datetime
import json
import os
import sys
from pathlib import Path
import numpy as np

from scipy.spatial.transform import Rotation


def rotate_matrix(input_matrix, axis, degrees):
    # convert degrees to radians
    theta = np.radians(degrees)
    # create a rotation matrix depending on the axis
    if axis == 'x':
        R = [[1, 0, 0, 0],
            [0, np.cos(theta), -np.sin(theta), 0],
            [0, np.sin(theta), np.cos(theta), 0],
            [0, 0, 0, 1]]
    elif axis == 'y':
        R = [[np.cos(theta), 0, np.sin(theta), 0],
            [0, 1, 0, 0],
            [-np.sin(theta), 0, np.cos(theta), 0],
            [0, 0, 0, 1]]
    elif axis == 'z':
        R = [[np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]
    else:
        print("Invalid axis. Please choose 'x', 'y', or 'z'.")
        return
    # multiply the rotation matrix with the input matrix
    output_matrix = np.dot(R, input_matrix)
    
    # return the rotated matrix
    return output_matrix

def conversion(matrix: np.ndarray):
    matrix = np.array(matrix)

    # matrix = rotate_matrix(matrix, 'y', 90)

    # Create a rotation matrix around the local X-axis
    rotation_matrix = Rotation.from_euler("Z", [270], degrees=True).as_matrix()

    # Extract the 3x3 submatrix from the object matrix
    orientation_matrix = matrix[:3, :3]

    # Multiply the rotation matrix with the orientation matrix
    new_orientation_matrix = rotation_matrix @ orientation_matrix

    # Replace the 3x3 submatrix in the object matrix with the new orientation matrix
    matrix[:3, :3] = new_orientation_matrix

    matrix = rotate_matrix(matrix, 'y', 90)
 

    # Create a rotation matrix around the local X-axis
    rotation_matrix = Rotation.from_euler("xz", [90, 90], degrees=True).as_matrix()

    # Extract the 3x3 submatrix from the object matrix
    orientation_matrix = matrix[:3, :3]

    # Multiply the rotation matrix with the orientation matrix
    new_orientation_matrix = rotation_matrix @ orientation_matrix

    # Replace the 3x3 submatrix in the object matrix with the new orientation matrix
    matrix[:3, :3] = new_orientation_matrix


    # Convert the numpy array to a list of lists and return the resulting matrix
    return matrix.tolist()

def convert(file_prefix: str = None):
    root_path = Path(os.curdir)
    run_path = root_path / 'runs/conversion_run'
    transforms_path = run_path / 'original_transforms.json'
    
    # Variables for 
    frames = None
    new_transforms = None
    new_frames = []

    with open(transforms_path, 'r') as f:
        new_transforms = json.load(f)
        frames = new_transforms['frames']

    num_convert = len(frames) / 1
    # Convert each frame with the conversion matrix
    for i, frame in enumerate(frames):
        if i < num_convert:
            new_transform = conversion(frame['transform_matrix'])
        else:
            new_transform = frame['transform_matrix']
        
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