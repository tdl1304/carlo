import numpy as np
import carla

def unreal_axis_2_blender_conversion(unreal_transform_matrix):
        # Step 1: Create a conversion matrix
        conversion_matrix = np.array([[1, 0, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, -1, 0, 0],
                                  [0, 0, 0, 1]])
        
        # Step 2: Multiply the transformation matrix with the conversion matrix
        transformed_matrix = np.matmul(conversion_matrix, unreal_transform_matrix)

        
        # Step 3: Flip the y and z coordinates of the resulting matrix
        transformed_matrix[1] = -transformed_matrix[1]
        transformed_matrix[2] = -transformed_matrix[2]

        # Step 3: Apply a 90 degree rotation around the Z-axis to the position
        # position = transformed_matrix[:3, 3]
        # rotation_matrix = np.array([[0, -1, 0, 0],
        #                             [1, 0, 0, 0],
        #                             [0, 0, 1, 0],
        #                             [0, 0, 0, 1]])
        # transformed_position = np.matmul(rotation_matrix, position)
        # transformed_matrix[:3, 3] = transformed_position

        # Step 3: Apply a 90 degree rotation around the Z-axis to the entire matrix
        # rotation_matrix = np.array([[0, -1, 0, 0],
        #                             [1, 0, 0, 0],
        #                             [0, 0, 1, 0],
        #                             [0, 0, 0, 1]])
        # transformed_matrix = np.matmul(rotation_matrix, transformed_matrix)
        
        # Convert the numpy array to a list of lists and return the resulting matrix
        return transformed_matrix.tolist()


def unreal_axis_2_blender_conversion_v2(unreal_transform_matrix):
    # Step 1: Create a conversion matrix to swap Y and Z
    swap_matrix = np.array([[1, 0, 0, 0],
                            [0, 0, 1, 0],
                            [0, -1, 0, 0],
                            [0, 0, 0, 1]])
    
    # Step 2: Create a rotation matrix to account for different axis conventions
    rotation_matrix = np.array([[0, -1, 0, 0],
                                [1, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
    
    # Step 3: Combine the matrices to form the final transformation matrix
    transformed_matrix = np.matmul(rotation_matrix, np.matmul(swap_matrix, unreal_transform_matrix))
    
    # Convert the numpy array to a list of lists and return the resulting matrix
    return transformed_matrix.tolist()


def unreal_axis_2_blender_conversion_v3(unreal_transform_matrix):
        # define the transformation matrix from Carla
        # location = carla.Location(x=100.0, y=50.0, z=0.0)
        # rotation = carla.Rotation(pitch=0.0, yaw=90.0, roll=0.0)
        # transform = carla.Transform(location, rotation)
        transform = unreal_transform_matrix

        # convert the matrix into the format used by NerfStudio
        transform_matrix = np.eye(4)
        transform_matrix[:3, :3] = np.array(transform.get_matrix())[:3, :3].T
        # transform_matrix[:3, 3] = -np.dot(transform_matrix[:3, :3], np.array([transform.location.x, transform.location.y, transform.location.z]))
        camera_position = np.array([transform.location.x, transform.location.y, transform.location.z])
        camera_position = np.dot(transform_matrix, np.append(camera_position, 1))
        transform_matrix[:3, 3] = -camera_position[:3]
        transform_matrix = transform_matrix.tolist()
        
        return transform_matrix

def unreal_axis_2_blender_conversion_v4(unreal_transform_matrix):
        # Step 1: Flip around X
        # matrix_1 = np.array([[0, 1, 0, 0],
        #                           [1, 0, 0, 0],
        #                           [0, 0, 1, 0],
        #                           [0, 0, 0, 1]])
        
        matrix_1 = np.array([[1, 0, 0, 0],
                        [0, 0, -1, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]])
        
        # Step 1: Flip around Z
        matrix_2 = np.array([[0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [-1, 0, 0, 0],
                        [0, 0, 0, 1]])

        # Step 1: Flip around Y
        matrix_3 = np.array([[0, -1, 0, 0],
                                [1, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        
        # Step 2: Multiply the transformation matrix with the conversion matrix
        transformed_matrix = np.matmul(matrix_1, unreal_transform_matrix)
        transformed_matrix = np.matmul(matrix_2, transformed_matrix)
        transformed_matrix = np.matmul(matrix_3, transformed_matrix)
        
        # # Step 3: Flip the y and z coordinates of the resulting matrix
        # transformed_matrix[0] = -transformed_matrix[0]
        # transformed_matrix[1] = -transformed_matrix[1]
        
        # Convert the numpy array to a list of lists and return the resulting matrix
        return transformed_matrix.tolist()


