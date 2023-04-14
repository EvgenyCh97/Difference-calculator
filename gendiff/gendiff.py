import gendiff.stylish as stylish
import json
import yaml
from yaml import CLoader as Loader


def get_dict_from_(file_path):
    if file_path.endswith('.yml') or file_path.endswith('.yaml'):
        return yaml.load(open(file_path), Loader=Loader)
    if file_path.endswith('.json'):
        return json.load(open(file_path))


def convert_bool_and_null_to_str(tree):
    for elem in tree:
        if type(tree[elem]) != dict:
            if tree[elem] is None:
                tree[elem] = 'null'
            elif tree[elem] is True:
                tree[elem] = 'true'
            elif tree[elem] is False:
                tree[elem] = 'false'
        else:
            children = tree[elem]
            convert_bool_and_null_to_str(children)
    return tree


def compare_files():
    def inner(dict1, dict2, depth=1):
        result = dict()
        for key in dict1.keys():
            if dict2.get(key) and type(dict1[key]) == dict and type(
                    dict2[key]) == dict:
                result[key] = {'type': 'nested',
                               'value': inner(dict1[key], dict2[key],
                                              depth + 1), 'depth': depth}
            elif dict2.get(key):
                if dict1[key] == dict2[key]:
                    result[key] = {'type': 'unchanged', 'value': dict1.get(key),
                                   'depth': depth}
                else:
                    if type(dict1[key]) == dict:
                        result[key] = {'type': 'changed',
                                       'value': dict2.get(key),
                                       'old_value': inner(dict1[key],
                                                          dict1[key],
                                                          depth + 1),
                                       'depth': depth}
                    elif type(dict2[key]) == dict:
                        result[key] = {'type': 'changed',
                                       'value': inner(dict2[key], dict2[key],
                                                      depth + 1),
                                       'old_value': dict1.get(key),
                                       'depth': depth}
                    else:
                        result[key] = {'type': 'changed',
                                       'value': dict2.get(key),
                                       'old_value': dict1.get(key),
                                       'depth': depth}
            else:
                if type(dict1[key]) == dict:
                    result[key] = {'type': 'deleted', 'value': inner(dict1[key],
                                                                     dict1[key],
                                                                     depth + 1),
                                   'depth': depth}
                else:
                    result[key] = {'type': 'deleted', 'value': dict1.get(key),
                                   'depth': depth}
        for key in dict2.keys():
            if dict1.get(key) is None:
                if type(dict2[key]) == dict:
                    result[key] = {'type': 'added',
                                   'value': inner(dict2.get(key),
                                                  dict2.get(key), depth + 1),
                                   'depth': depth}
                else:
                    result[key] = {'type': 'added', 'value': dict2.get(key),
                                   'depth': depth}
        return result
    return inner


def generate_diff(file_path1, file_path2):
    dict1 = convert_bool_and_null_to_str(get_dict_from_(file_path1))
    dict2 = convert_bool_and_null_to_str(get_dict_from_(file_path2))
    compare = compare_files()
    diff = '{\n'
    result_list = stylish.get_stylish(compare(dict1, dict2))
    for string in result_list:
        if string == result_list[-1]:
            diff += string
        else:
            diff += string + '\n'
    return diff.replace('"', '')
