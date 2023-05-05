import json


def get_plain(target_dict):
    result = list()

    def inner(comparison_dict, path=[]):
        sorted_keys = sorted(comparison_dict)
        for key in sorted_keys:

            value = converter(comparison_dict[key]['value'])
            depth = comparison_dict[key]['depth']
            key_type = comparison_dict[key]['type']

            if depth == 1:
                path = []
            if key_type == 'nested':
                path.append(f'{key}.')
                inner(value, path)
            if key_type == 'changed':
                old_value = converter(comparison_dict[key]['old_value'])
                if type(comparison_dict[key]['old_value']) == dict:
                    result.append(f'Property \'{"".join(path)}{key}\' was '
                                  f'updated. From [complex value] to {value}')
                elif type(value) == dict:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was updated. From {old_value} to '
                                  f'[complex value]')
                else:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was updated. From {old_value} to {value}')
            if key_type == 'deleted':
                result.append(f'Property \'{"".join(path)}{key}\' was removed')
            if key_type == 'added':
                if type(value) == dict:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was added with value: [complex value]')
                else:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was added with value: {value}')
            if key == sorted_keys[-1] and path:
                path.pop()

    inner(target_dict)
    return result


def converter(value):
    if type(value) not in [int, float, dict]:
        return json.dumps(value).replace('"', "'")
    else:
        return value
