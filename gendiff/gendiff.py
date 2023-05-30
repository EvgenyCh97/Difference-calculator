import json
import yaml
import os
from gendiff.formatters import stylish, plain
from gendiff.formatters.json import get_json
from yaml import CLoader as Loader


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def get_data(file_path):
    lines = read_file(file_path)
    result = ''.join(lines)
    file_format = os.path.splitext(file_path)[-1]
    if file_format in ['.yaml', '.yml']:
        return yaml.load(result, Loader=Loader)
    if file_format == '.json':
        return json.loads(result)


def get_diff(dict1, dict2):
    diff = dict()
    keys_set1, keys_set2 = set(dict1.keys()), set(dict2.keys())
    keys_concatenation = keys_set1.union(keys_set2)
    added_keys = keys_set2.difference(keys_set1)
    for key in keys_concatenation:
        value1 = dict1.get(key)
        value2 = dict2.get(key)
        if type(value1) == dict and type(value2) == dict:
            diff[key] = {'type': 'nested', 'value': get_diff(value1, value2)}
        elif key in dict2.keys():
            if value1 == value2:
                diff[key] = {'type': 'unchanged', 'value': value1}
            else:
                diff[key] = {'type': 'changed', 'new_value': value2,
                             'old_value': value1}
        else:
            diff[key] = {'type': 'deleted', 'value': value1}
        if key in added_keys:
            diff[key] = {'type': 'added', 'value': value2}
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    dict1 = get_data(file_path1)
    dict2 = get_data(file_path2)
    diff = get_diff(dict1, dict2)
    if format_name == 'stylish':
        return stylish.get_stylish(diff)
    if format_name == 'plain':
        return plain.get_plain(diff)
    if format_name == 'json':
        return get_json(diff)
