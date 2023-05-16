import json


def get_plain(diff_dict):
    result = ''
    diff_list = list()
    complete_diff_list(diff_dict, diff_list)
    for string in diff_list:
        if string == diff_list[-1]:
            result += string
        else:
            result += string + '\n'
    return result


def complete_diff_list(diff_dict, diff_list, path=[], depth_lvl=1):
    sorted_keys = sorted(diff_dict)
    for key in sorted_keys:

        value = converter(diff_dict[key]['value'])
        key_type = diff_dict[key]['type']

        if depth_lvl == 1:
            path = []
        if key_type == 'nested':
            path.append(f'{key}.')
            complete_diff_list(value, diff_list, path, depth_lvl + 1)
        if key_type == 'changed':
            old_value = converter(diff_dict[key]['old_value'])
            if type(old_value) == dict:
                diff_list.append(f'Property \'{"".join(path)}{key}\' was '
                                 f'updated. From [complex value] to {value}')
            elif type(value) == dict:
                diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                 f'was updated. From {old_value} to '
                                 f'[complex value]')
            else:
                diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                 f'was updated. From {old_value} to {value}')
        if key_type == 'deleted':
            diff_list.append(f'Property \'{"".join(path)}{key}\' was removed')
        if key_type == 'added':
            if type(value) == dict:
                diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                 f'was added with value: [complex value]')
            else:
                diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                 f'was added with value: {value}')
        if key == sorted_keys[-1] and path:
            path.pop()


def converter(value):
    if type(value) not in [int, float, dict]:
        return json.dumps(value).replace('"', "'")
    else:
        return value
