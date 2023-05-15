import json


def get_json(diff):
    return json.dumps(diff, sort_keys=True)
