import json
import yaml
from yaml import CLoader as Loader
import gendiff.stylish as stylish


def get_dict_from_(file_path):
    if file_path.endswith('.yml') or file_path.endswith('.yaml'):
        return yaml.load(open(file_path), Loader=Loader)
    if file_path.endswith('.json'):
        return json.load(open(file_path))


def encode_(encoded_list):
    return json.dumps(dict(encoded_list), indent=2)


def sort_(sortable_dict):
    sorted_keys = sorted(sortable_dict, key=lambda items: items[2])
    return [(key, sortable_dict[key]) for key in sorted_keys]


def get_result_list(file_path1, file_path2):
    dict1 = get_dict_from_(file_path1)
    dict2 = get_dict_from_(file_path2)
    result = dict()
    for key in dict1.keys():
        if dict2.get(key):
            if dict1[key] == dict2[key]:
                result[f'  {key}'] = dict1.get(key)
            else:
                result[f'- {key}'] = dict1.get(key)
                result[f'+ {key}'] = dict2.get(key)
        else:
            result[f'- {key}'] = dict1.get(key)
    for key in dict2.keys():
        if dict1.get(key) is None:
            result[f'+ {key}'] = dict2[key]
    return result


def generate_diff(file_path1, file_path2):
    return encode_(sort_(get_result_list(
        file_path1, file_path2))).replace('"', '').replace(',', '')
