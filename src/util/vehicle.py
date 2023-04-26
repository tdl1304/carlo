import carla


def get_back_axle_position(vehicle: carla.Vehicle) -> carla.Vector3D:
    wheels = vehicle.get_physics_control().wheels

    back_left_wheel, back_right_wheel = wheels[2], wheels[3]

    back_axle_middle = (back_left_wheel.position + back_right_wheel.position) / 2
    back_axle_middle /= 100  # cm to m

    return back_axle_middle
