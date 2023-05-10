import json
import yaml
from gendiff.formatters import stylish, plain
from gendiff.formatters.json import get_json
from yaml import CLoader as Loader


def get_dict_from_(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            return yaml.load(file, Loader=Loader)
        if file_path.endswith('.json'):
            return json.load(file)


def convert_value_to_str(tree):
    for node in tree:
        value = tree[node]
        if type(value) != dict:
            if type(value) in [int, float]:
                pass
            else:
                tree[node] = json.dumps(value).replace('"', '')
        else:
            children = value
            convert_value_to_str(children)
    return tree


def compare_files(dict1, dict2, depth=1):
    result = dict()
    for key in dict1.keys():
        if key in dict2.keys() and type(dict1.get(key)) == dict and type(
                dict2.get(key)) == dict:
            result[key] = {'type': 'nested',
                           'value': compare_files(dict1.get(key),
                                                  dict2.get(key),
                                                  depth + 1), 'depth': depth}
        elif key in dict2.keys():
            if dict1.get(key) == dict2.get(key):
                result[key] = {'type': 'unchanged', 'value': dict1.get(key),
                               'depth': depth}
            else:
                if type(dict1.get(key)) == dict:
                    result[key] = {'type': 'changed',
                                   'value': dict2.get(key),
                                   'old_value': compare_files(dict1.get(key),
                                                              dict1.get(key),
                                                              depth + 1),
                                   'depth': depth}
                elif type(dict2.get(key)) == dict:
                    result[key] = {'type': 'changed',
                                   'value': compare_files(dict2.get(key),
                                                          dict2.get(key),
                                                          depth + 1),
                                   'old_value': dict1.get(key),
                                   'depth': depth}
                else:
                    result[key] = {'type': 'changed',
                                   'value': dict2.get(key),
                                   'old_value': dict1.get(key),
                                   'depth': depth}
        else:
            if type(dict1.get(key)) == dict:
                result[key] = {'type': 'deleted',
                               'value': compare_files(dict1.get(key),
                                                      dict1.get(key),
                                                      depth + 1),
                               'depth': depth}
            else:
                result[key] = {'type': 'deleted', 'value': dict1.get(key),
                               'depth': depth}
    added_keys = set(dict2)
    added_keys.difference_update(set(dict1))
    for key in added_keys:
        if type(dict2[key]) == dict:
            result[key] = {'type': 'added',
                           'value': compare_files(dict2.get(key),
                                                  dict2.get(key), depth + 1),
                           'depth': depth}
        else:
            result[key] = {'type': 'added', 'value': dict2.get(key),
                           'depth': depth}
    return result


def generate_diff(file_path1, file_path2, format_name='stylish'):
    dict1 = get_dict_from_(file_path1)
    dict2 = get_dict_from_(file_path2)
    compare = compare_files(dict1, dict2)
    if format_name == 'stylish':
        diff = '{\n'
        result_list = stylish.get_stylish(compare)
    if format_name == 'plain':
        diff = ''
        result_list = plain.get_plain(compare)
    if format_name == 'json':
        return get_json(compare)
    for string in result_list:
        if string == result_list[-1]:
            diff += string
        else:
            diff += string + '\n'
    return diff
