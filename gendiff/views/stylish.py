def get_stylish(target_dict):
    result = list()

    def inner(comparison_dict):
        sorted_keys = sorted(comparison_dict)
        for key in sorted_keys:
            depth = comparison_dict[key]['depth']
            if comparison_dict[key]['type'] == 'nested':
                children = comparison_dict[key]['value']
                result.append(f'{" " * (4 * depth - 2)}  {key}: ' + '{')
                inner(children)
            if comparison_dict[key]['type'] == 'changed':
                value = comparison_dict[key]['value']
                old_value = comparison_dict[key]['old_value']
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
            if comparison_dict[key]['type'] == 'unchanged':
                value = comparison_dict[key]['value']
                result.append(f'{" " * (4 * depth - 2)}  {key}: {value}')
            if comparison_dict[key]['type'] == 'deleted':
                if type(comparison_dict[key]['value']) == dict:
                    children = comparison_dict[key]['value']
                    result.append(f'{" " * (4 * depth - 2)}- {key}: ' + '{')
                    inner(children)
                else:
                    value = comparison_dict[key]['value']
                    result.append(f'{" " * (4 * depth - 2)}- {key}: {value}')
            if comparison_dict[key]['type'] == 'added':
                if type(comparison_dict[key]['value']) == dict:
                    children = comparison_dict[key]['value']
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: ' + '{')
                    inner(children)
                else:
                    value = comparison_dict[key]['value']
                    result.append(f'{" " * (4 * depth - 2)}+ {key}: {value}')
            if key == sorted_keys[-1]:
                result.append(f'{" " * 4 * (depth - 1)}' + '}')

    inner(target_dict)
    return result
