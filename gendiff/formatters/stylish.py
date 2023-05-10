import json


def get_stylish(diff_dict):
    result = '{\n'
    diff_list = list()
    complete_diff_list(diff_dict, diff_list)
    for string in diff_list:
        if string == diff_list[-1]:
            result += string
        else:
            result += string + '\n'
    return result


def complete_diff_list(diff_dict, diff_list):
    sorted_keys = sorted(diff_dict)
    for key in sorted_keys:

        value = converter(diff_dict[key]['value'])
        depth = diff_dict[key]['depth']
        key_type = diff_dict[key]['type']

        if key_type == 'nested':
            diff_list.append(f'{" " * (4 * depth - 2)}  {key}: ' + '{')
            complete_diff_list(value, diff_list)
        if key_type == 'changed':
            old_value = converter(diff_dict[key]['old_value'])
            if type(old_value) == dict:
                diff_list.append(f'{" " * (4 * depth - 2)}- {key}: ' + '{')
                complete_diff_list(old_value, diff_list)
            else:
                diff_list.append(
                    f'{" " * (4 * depth - 2)}- {key}: {old_value}')
            if type(value) == dict:
                diff_list.append(f'{" " * (4 * depth - 2)}+ {key}: ' + '{')
                complete_diff_list(value, diff_list)
            else:
                diff_list.append(f'{" " * (4 * depth - 2)}+ {key}: {value}')
        if key_type == 'unchanged':
            diff_list.append(f'{" " * (4 * depth - 2)}  {key}: {value}')
        if key_type == 'deleted':
            if type(value) == dict:
                diff_list.append(f'{" " * (4 * depth - 2)}- {key}: ' + '{')
                complete_diff_list(value, diff_list)
            else:
                diff_list.append(f'{" " * (4 * depth - 2)}- {key}: {value}')
        if key_type == 'added':
            if type(value) == dict:
                diff_list.append(f'{" " * (4 * depth - 2)}+ {key}: ' + '{')
                complete_diff_list(value, diff_list)
            else:
                diff_list.append(f'{" " * (4 * depth - 2)}+ {key}: {value}')
        if key == sorted_keys[-1]:
            diff_list.append(f'{" " * 4 * (depth - 1)}' + '}')


def converter(value):
    if type(value) not in [int, float, dict]:
        return json.dumps(value).replace('"', '')
    else:
        return value
