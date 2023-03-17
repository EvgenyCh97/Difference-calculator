import json
import yaml
from yaml import CLoader as Loader


def get_dict_from_(file_path):
    if file_path.endswith('.yml') or file_path.endswith('.yaml'):
        return yaml.load(open(file_path), Loader=Loader)
    if file_path.endswith('.json'):
        return json.load(open(file_path))


def encode_(encoded_list):
    return json.dumps(dict(encoded_list), indent=2)


def sort_(sortable_list):
    return sorted(sortable_list, key=lambda items: items[0][2])


def get_result_list(file_path1, file_path2):
    dict1 = get_dict_from_(file_path1)
    dict2 = get_dict_from_(file_path2)
    result = []
    for key in dict1.keys():
        if dict2.get(key):
            if dict1[key] == dict2[key]:
                result.append((f'  {key}', dict1.get(key)))
            else:
                result.append((f'- {key}', dict1.get(key)))
                result.append((f'+ {key}', dict2.get(key)))
        else:
            result.append((f'- {key}', dict1.get(key)))
    for key in dict2.keys():
        if dict1.get(key) is None:
            result.append((f'+ {key}', dict2.get(key)))
    return result


def generate_diff(file_path1, file_path2):
    return encode_(sort_(get_result_list(
        file_path1, file_path2))).replace('"', '').replace(',', '')
