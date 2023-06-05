import json


def get_plain(diff_dict):
    diff_list = complete_plain_list(diff_dict)
    return '\n'.join(diff_list)


def complete_plain_list(diff_dict):
    diff_list = list()
    path = list()

    def inner(node, depth_lvl=1):
        nonlocal path
        sorted_keys = sorted(node)
        for key in sorted_keys:
            key_type = node[key]['type']
            if depth_lvl == 1:
                path = []
            if key_type == 'changed':
                old_value = convert_to_plain(node[key]['old_value'])
                new_value = convert_to_plain(node[key]['new_value'])
                diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                 f'was updated. From {old_value} '
                                 f'to {new_value}')
            else:
                value = convert_to_plain(node[key]['value'])
                if key_type == 'nested':
                    path.append(f'{key}.')
                    children = node[key]['value']
                    inner(children, depth_lvl + 1)
                if key_type == 'deleted':
                    diff_list.append(f'Property \'{"".join(path)}{key}\' was '
                                     f'removed')
                if key_type == 'added':
                    diff_list.append(f'Property \'{"".join(path)}{key}\' '
                                     f'was added with value: {value}')
            if key == sorted_keys[-1] and path:
                path.pop()
    inner(diff_dict)
    return diff_list


def convert_to_plain(value):
    if type(value) == dict:
        return '[complex value]'
    elif type(value) not in [int, float]:
        return json.dumps(value).replace('"', "'")
    else:
        return value
