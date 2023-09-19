import json
import yaml
import os
from gendiff.formatters import stylish, plain
from gendiff.formatters.json import get_json
from yaml import CLoader as Loader


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def get_file_extension(file_path):
    return os.path.splitext(file_path)[-1]


def parse(content, extension):
    if extension in ['.yaml', '.yml']:
        return yaml.load(content, Loader=Loader)
    if extension == '.json':
        return json.loads(content)


def get_diff(dict1, dict2):
    diff = dict()
    keys_set1, keys_set2 = set(dict1.keys()), set(dict2.keys())
    all_keys = keys_set1.union(keys_set2)
    for key in all_keys:
        value1 = dict1.get(key)
        value2 = dict2.get(key)
        if type(value1) == dict and type(value2) == dict:
            diff[key] = {'type': 'nested', 'value': get_diff(value1, value2)}
        elif key in dict1.keys() and key in dict2.keys():
            if value1 == value2:
                diff[key] = {'type': 'unchanged',
                             'value': value1}
            else:
                diff[key] = {'type': 'changed',
                             'new_value': value2,
                             'old_value': value1}
        elif key in dict1.keys():
            diff[key] = {'type': 'deleted',
                         'value': value1}
        elif key in dict2.keys():
            diff[key] = {'type': 'added',
                         'value': value2}
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    content1, ext1 = read_file(file_path1), get_file_extension(file_path1)
    content2, ext2 = read_file(file_path2), get_file_extension(file_path2)
    dict1 = parse(content1, ext1)
    dict2 = parse(content2, ext2)
    diff = get_diff(dict1, dict2)
    if format_name == 'stylish':
        return stylish.get_stylish(diff)
    if format_name == 'plain':
        return plain.get_plain(diff)
    if format_name == 'json':
        return get_json(diff)
