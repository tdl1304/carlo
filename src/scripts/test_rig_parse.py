from src.common.rig import parse_rig_json

rig = parse_rig_json("rig.json")
print(len(rig.sensors))