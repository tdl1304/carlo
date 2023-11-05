from pydantic import BaseModel, Field, root_validator, validator

from typing import List, Optional, Union, Any


class FThetaProperties(BaseModel):
    model: str = Field(..., alias="Model")
    bw_poly: str = Field(..., alias="bw-poly")
    cx: float
    cy: float
    height: int
    width: int


class OcamProperties(BaseModel):
    model: str = Field(..., alias="Model")
    c: float
    cx: float
    cy: float
    d: float
    e: float
    height: int
    poly: str
    width: int


class NominalSensor2Rig(BaseModel):
    roll_pitch_yaw: List[float] = Field(..., alias="roll-pitch-yaw")
    translation: List[float] = Field(..., alias="t")

    @property
    def roll(self) -> float:
        return self.roll_pitch_yaw[0]

    @property
    def pitch(self) -> float:
        return self.roll_pitch_yaw[1]

    @property
    def yaw(self) -> float:
        return self.roll_pitch_yaw[2]

    @property
    def x(self) -> float:
        return self.translation[0]

    @property
    def y(self) -> float:
        return self.translation[1]

    @property
    def z(self) -> float:
        return self.translation[2]


class Sensor(BaseModel):
    name: str
    nominal_sensor_2_rig: NominalSensor2Rig = Field(..., alias="nominalSensor2Rig_FLU")
    parameter: str
    properties: Union[None, FThetaProperties, OcamProperties]
    protocol: str
        
    @property
    def is_camera(self) -> bool:
        return "camera" in self.protocol

    @property
    def fov(self) -> int:
        known_fovs = {
            'C1_front60Single': 60,
            'C2_tricam60': 60,
            'C3_tricam120': 120,
            'C6_L1': 120,
            'C7_L2': 120,
            'C5_R1': 120,
            'C8_R2': 120,
            'C4_rearCam': 120,
        }
        if self.name in known_fovs:
            return known_fovs[self.name]
        if '60' in self.name:
            return 60
        return 120


class Actuation(BaseModel):
    brake_actuator_time_constant: float = Field(..., alias="brakeActuatorTimeConstant")
    brake_actuator_time_delay: float = Field(..., alias="brakeActuatorTimeDelay")
    drive_by_wire_time_constant: float = Field(..., alias="driveByWireTimeConstant")
    drive_by_wire_time_delay: float = Field(..., alias="driveByWireTimeDelay")
    effective_mass: float = Field(..., alias="effectiveMass")
    max_sterring_wheel_angle: float = Field(..., alias="maxSteeringWheelAngle")
    steering_wheel_to_steering_map: List[float] = Field(
        ..., alias="steeringWheelToSteeringMap"
    )
    trottle_actuator_time_constant: float = Field(
        ..., alias="throttleActuatorTimeConstant"
    )
    trottle_actuator_time_delay: float = Field(..., alias="throttleActuatorTimeDelay")
    torque_lut: Any = Field(..., alias="torqueLUT")


class Axle(BaseModel):
    cornering_stiffness: float = Field(..., alias="corneringStiffness")
    position: float
    track: float
    wheel_radius_left: float = Field(..., alias="wheelRadiusLeft")
    wheel_radius_right: float = Field(..., alias="wheelRadiusRight")


class VehicleBody(BaseModel):
    bounding_box_position: List[float] = Field(..., alias="boundingBoxPosition")
    center_Of_mass: List[float] = Field(..., alias="centerOfMass")
    height: float
    inertia: List[float]
    length: float
    mass: float
    width: float
    width_without_mirrors: float = Field(..., alias="widthWithoutMirrors")


class VehicleValue(BaseModel):
    actuation: Actuation
    axle_front: Axle = Field(..., alias="axleFront")
    axle_rear: Axle = Field(..., alias="axleRear")
    body: VehicleBody
    has_cabin: bool = Field(..., alias="hasCabin")
    num_trailers: int = Field(..., alias="numTrailers")


class Vehicle(BaseModel):
    valid: bool
    value: VehicleValue


class Rig(BaseModel):
    sensors: List[Sensor]
    # vehicle: Optional[Vehicle]
    # vehicleio: Optional[List[Any]]

    @validator("sensors", pre=True, always=True)
    def filter_items(cls, items: List[Sensor]):
        filtered = [item for item in items if "camera" in item["protocol"]]
        return filtered


class RigFile(BaseModel):
    rig: Rig
    version: int


def parse_rig_json(path: str):
    return RigFile.parse_file(path).rig
   
