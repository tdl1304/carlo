from typing import List
from src.common.rig import Rig, Sensor
from src.sensors.camera import CameraSettings
from src.sensors.camera_rig import CameraRig
from src.util.vehicle import get_back_axle_position
import carla


def make_sensor_transform(sensor: Sensor, sensor_offset: carla.Vector3D):
    return carla.Transform(
        carla.Location(
            x=sensor.nominal_sensor_2_rig.x,
            y=-sensor.nominal_sensor_2_rig.y,
            z=sensor.nominal_sensor_2_rig.z,
        ) + sensor_offset,
        carla.Rotation(
            pitch=sensor.nominal_sensor_2_rig.pitch,
            yaw=-sensor.nominal_sensor_2_rig.yaw,
            roll=sensor.nominal_sensor_2_rig.roll,
        ),
    )


def create_camera_rigs_from_rig(ego: carla.Actor, rig: Rig, scale: int = 2) -> List[CameraRig]:
    cameras = list(filter(lambda sensor: sensor.is_camera, rig.sensors))
    ego_tf = ego.get_transform()
    back_axle_position = get_back_axle_position(ego)
    back_axle_offset = back_axle_position - ego_tf.location

    sensor_offset = carla.Vector3D(
        x=back_axle_offset.dot(ego_tf.get_forward_vector()),
        y=back_axle_offset.dot(ego_tf.get_right_vector()),
        z=back_axle_offset.dot(ego_tf.get_up_vector()),
    )

    camera_rigs = []
    for sensor in cameras:
        camera_rig = CameraRig(transform=make_sensor_transform(sensor=sensor, sensor_offset=sensor_offset), camera_settings=CameraSettings(
            fov=sensor.fov,
            image_size_x=sensor.properties.width // scale,
            image_size_y=sensor.properties.height // scale,
        ))
        camera_rig.create_camera(ego)
        camera_rigs.append(camera_rig)
    
    return camera_rigs
