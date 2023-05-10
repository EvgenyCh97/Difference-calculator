import json


def get_json(target_dict):
    return json.dumps(target_dict, sort_keys=True)
