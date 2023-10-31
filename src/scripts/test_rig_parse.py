from src.common.rig import Rig, Sensor, parse_rig_json

rig = parse_rig_json("rig.json")
print(rig)