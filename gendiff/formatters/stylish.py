import json


def get_stylish(target_dict):
    result = list()

    def inner(comparison_dict):
        sorted_keys = sorted(comparison_dict)
        for key in sorted_keys:

            value = converter(comparison_dict[key]['value'])
            depth = comparison_dict[key]['depth']
            key_type = comparison_dict[key]['type']

            if key_type == 'nested':
                result.append(f'{" " * (4 * depth - 2)}  {key}: ' + '{')
                inner(value)
            if key_type == 'changed':
                old_value = converter(comparison_dict[key]['old_value'])
                if type(old_value) == dict:
                    result.append(f'{" " * (4 * depth - 2)}- {key}: ' + '{')
                    inner(old_value)
                else:
                    result.append(
                        f'{" " * (4 * depth - 2)}- {key}: {old_value}')
                if type(value) == dict:
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: ' + '{')
                    inner(value)
                else:
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: {value}')
            if key_type == 'unchanged':
                result.append(f'{" " * (4 * depth - 2)}  {key}: {value}')
            if key_type == 'deleted':
                if type(value) == dict:
                    result.append(f'{" " * (4 * depth - 2)}- {key}: ' + '{')
                    inner(value)
                else:
                    result.append(f'{" " * (4 * depth - 2)}- {key}: {value}')
            if key_type == 'added':
                if type(value) == dict:
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: ' + '{')
                    inner(value)
                else:
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: {value}')
            if key == sorted_keys[-1]:
                result.append(f'{" " * 4 * (depth - 1)}' + '}')

    inner(target_dict)
    return result


def converter(value):
    if type(value) not in [int, float, dict]:
        return json.dumps(value).replace('"', '')
    else:
        return value
