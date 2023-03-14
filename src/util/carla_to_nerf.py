import carla

def carla_to_nerf(camera_transform: carla.Transform):
    unreal_location = camera_transform.location
    unreal_rotation = camera_transform.rotation

    # Convert from Unreal Engine to Blender coordinate system
    # From Carla Docs: Warning: The declaration order is different in CARLA (pitch,yaw,roll), and in the Unreal Engine Editor (roll,pitch,yaw). When working in a build from source, don't mix up the axes' rotations.
    blender_matrix = carla.Transform(
        carla.Location(x=-unreal_location.z, y=unreal_location.x, z=unreal_location.y),
        carla.Rotation(pitch=unreal_rotation.yaw + 90, yaw=unreal_rotation.roll + 90, roll=unreal_rotation.pitch)
    )
    
    return blender_matrix.get_matrix()