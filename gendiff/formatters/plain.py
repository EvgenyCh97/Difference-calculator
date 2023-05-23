import json


def get_plain(diff_dict):
    diff_list = complete_diff_list(diff_dict, list())
    return '\n'.join(diff_list)


def complete_diff_list(diff_dict, diff_list: list, path=[], depth_lvl=1):
    sorted_keys = sorted(diff_dict)
    for key in sorted_keys:

        value = converter(diff_dict[key]['value'])
        key_type = diff_dict[key]['type']

        if depth_lvl == 1:
            path = []
        if key_type == 'nested':
            path.append(f'{key}.')
            children = diff_dict[key]['value']
            complete_diff_list(children, diff_list, path, depth_lvl + 1)
        if key_type == 'changed':
            old_value = converter(diff_dict[key]['old_value'])
            diff_list.append(f'Property \'{"".join(path)}{key}\' '
                             f'was updated. From {old_value} to {value}')
        if key_type == 'deleted':
            diff_list.append(f'Property \'{"".join(path)}{key}\' was removed')
        if key_type == 'added':
            diff_list.append(f'Property \'{"".join(path)}{key}\' '
                             f'was added with value: {value}')
        if key == sorted_keys[-1] and path:
            path.pop()
    return diff_list


def converter(value):
    if type(value) == dict:
        return '[complex value]'
    elif type(value) not in [int, float]:
        return json.dumps(value).replace('"', "'")
    else:
        return value
