import json
import yaml
from gendiff.formatters import stylish, plain
from gendiff.formatters.json import get_json
from yaml import CLoader as Loader


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def get_dict_from(file_path):
    lines = read_file(file_path)
    result = ''.join(lines)
    if file_path.endswith('.yml') or file_path.endswith('.yaml'):
        return yaml.load(result, Loader=Loader)
    if file_path.endswith('.json'):
        return json.loads(result)


def get_diff_dict(dict1, dict2, depth=1):
    diff_dict = dict()
    for key in dict1.keys():
        if key in dict2.keys() and type(dict1.get(key)) == dict and type(
                dict2.get(key)) == dict:
            diff_dict[key] = {'type': 'nested',
                              'value': get_diff_dict(dict1.get(key),
                                                     dict2.get(key),
                                                     depth + 1), 'depth': depth}
        elif key in dict2.keys():
            if dict1.get(key) == dict2.get(key):
                diff_dict[key] = {'type': 'unchanged', 'value': dict1.get(key),
                                  'depth': depth}
            else:
                if type(dict1.get(key)) == dict:
                    diff_dict[key] = {'type': 'changed',
                                      'value': dict2.get(key),
                                      'old_value': get_diff_dict(dict1.get(key),
                                                                 dict1.get(key),
                                                                 depth + 1),
                                      'depth': depth}
                elif type(dict2.get(key)) == dict:
                    diff_dict[key] = {'type': 'changed',
                                      'value': get_diff_dict(dict2.get(key),
                                                             dict2.get(key),
                                                             depth + 1),
                                      'old_value': dict1.get(key),
                                      'depth': depth}
                else:
                    diff_dict[key] = {'type': 'changed',
                                      'value': dict2.get(key),
                                      'old_value': dict1.get(key),
                                      'depth': depth}
        else:
            if type(dict1.get(key)) == dict:
                diff_dict[key] = {'type': 'deleted',
                                  'value': get_diff_dict(dict1.get(key),
                                                         dict1.get(key),
                                                         depth + 1),
                                  'depth': depth}
            else:
                diff_dict[key] = {'type': 'deleted', 'value': dict1.get(key),
                                  'depth': depth}
    added_keys = set(dict2)
    added_keys.difference_update(set(dict1))
    for key in added_keys:
        if type(dict2[key]) == dict:
            diff_dict[key] = {'type': 'added',
                              'value': get_diff_dict(dict2.get(key),
                                                     dict2.get(key), depth + 1),
                              'depth': depth}
        else:
            diff_dict[key] = {'type': 'added', 'value': dict2.get(key),
                              'depth': depth}
    return diff_dict


def generate_diff(file_path1, file_path2, format_name='stylish'):
    dict1 = get_dict_from(file_path1)
    dict2 = get_dict_from(file_path2)
    if format_name == 'stylish':
        return stylish.get_stylish(get_diff_dict(dict1, dict2))
    if format_name == 'plain':
        return plain.get_plain(get_diff_dict(dict1, dict2))
    if format_name == 'json':
        return get_json(get_diff_dict(dict1, dict2))
