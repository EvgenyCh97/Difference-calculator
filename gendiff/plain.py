def get_plain(target_dict):
    result = list()

    def inner(comparison_dict, path=[]):
        sorted_keys = sorted(comparison_dict)
        for key in sorted_keys:
            current_depth = comparison_dict[key]['depth']
            if current_depth == 1:
                path = []
            if comparison_dict[key]['value'] in ['true', 'false', 'null']:
                value = comparison_dict[key]['value']
            else:
                value = f'\'{comparison_dict[key]["value"]}\''
            if comparison_dict[key]['type'] == 'nested':
                children = comparison_dict[key]['value']
                path.append(f'{key}.')
                inner(children, path)
            if comparison_dict[key]['type'] == 'changed':
                if comparison_dict[key]['old_value'] in ['true', 'false',
                                                         'null']:
                    old_value = comparison_dict[key]['old_value']
                else:
                    old_value = f'\'{comparison_dict[key]["old_value"]}\''
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
            if comparison_dict[key]['type'] == 'deleted':
                result.append(f'Property \'{"".join(path)}{key}\' was removed')
            if comparison_dict[key]['type'] == 'added':
                if type(comparison_dict[key]['value']) == dict:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was added with value: [complex value]')
                else:
                    result.append(f'Property \'{"".join(path)}{key}\' '
                                  f'was added with value: {value}')
            if key == sorted_keys[-1] and path:
                path.pop()

    inner(target_dict)
    return result
