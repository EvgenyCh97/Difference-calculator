import json

SPACES_PER_LVL = 4
LEFT_SHIFT = 2


def get_stylish(diff_dict):
    diff_list = complete_stylish_list(diff_dict, list())
    return '{\n' + '\n'.join(diff_list)


def complete_stylish_list(diff_dict, diff_list: list, depth_lvl=1):
    sorted_keys = sorted(diff_dict)
    for key in sorted_keys:
        value = convert_to_json(diff_dict[key]['value'])
        key_type = diff_dict[key]['type']
        if key_type == 'nested':
            form_string(diff_list, key, key_type, value, depth_lvl, '  ')
        if key_type == 'changed':
            old_value = convert_to_json(diff_dict[key]['old_value'])
            form_string(diff_list, key, key_type, old_value, depth_lvl, '- ')
            form_string(diff_list, key, key_type, value, depth_lvl, '+ ')
        if key_type == 'unchanged':
            form_string(diff_list, key, key_type, value, depth_lvl, '  ')
        if key_type == 'deleted':
            form_string(diff_list, key, key_type, value, depth_lvl, '- ')
        if key_type == 'added':
            form_string(diff_list, key, key_type, value, depth_lvl, '+ ')
        if key == sorted_keys[-1]:
            diff_list.append(f'{" " * SPACES_PER_LVL * (depth_lvl - 1)}' + '}')
    return diff_list


def form_string(diff_list, key, key_type, value, depth_lvl, spec_char):
    from gendiff.gendiff import get_diff
    if type(value) == dict:
        diff_list.append(
            f'{" " * (SPACES_PER_LVL * depth_lvl - LEFT_SHIFT)}{spec_char}'
            f'{key}: ' + '{')
        if key_type == 'nested':
            complete_stylish_list(value, diff_list, depth_lvl + 1)
        else:
            complete_stylish_list(get_diff(value, value), depth_lvl + 1)
    else:
        diff_list.append(
            f'{" " * (SPACES_PER_LVL * depth_lvl - LEFT_SHIFT)}{spec_char}'
            f'{key}: {value}')


def convert_to_json(value):
    if type(value) not in [int, float, dict]:
        return json.dumps(value).replace('"', "")
    else:
        return value
