SPACES_PER_LVL = 4
LEFT_SHIFT = 2


def get_stylish(diff_dict):
    diff_list = complete_stylish_list(diff_dict)
    return '{\n' + '\n'.join(diff_list)


def complete_stylish_list(diff_dict):
    diff_list = list()

    def inner(node, depth_lvl=1):
        sorted_keys = sorted(node)
        for key in sorted_keys:
            key_type = node[key]['type']
            if key_type == 'changed':
                old_value = convert_to_json(node[key]['old_value'])
                new_value = convert_to_json(node[key]['new_value'])
                diff_list.append(form_string(key, old_value, depth_lvl, '- '))
                if type(old_value) == dict:
                    inner(old_value, depth_lvl + 1)
                diff_list.append(form_string(key, new_value, depth_lvl, '+ '))
                if type(new_value) == dict:
                    inner(new_value, depth_lvl + 1)
            else:
                value = convert_to_json(node[key]['value'])
                if key_type == 'nested':
                    diff_list.append(form_string(key, value, depth_lvl, '  '))
                if key_type == 'unchanged':
                    diff_list.append(form_string(key, value, depth_lvl, '  '))
                if key_type == 'deleted':
                    diff_list.append(form_string(key, value, depth_lvl, '- '))
                if key_type == 'added':
                    diff_list.append(form_string(key, value, depth_lvl, '+ '))
                if type(value) == dict:
                    inner(value, depth_lvl + 1)
            if key == sorted_keys[-1]:
                diff_list.append(
                    f'{" " * SPACES_PER_LVL * (depth_lvl - 1)}' + '}')

    inner(diff_dict)
    return diff_list


def form_string(key, value, depth_lvl, spec_char):
    if type(value) == dict:
        return f'{" " * (SPACES_PER_LVL * depth_lvl - LEFT_SHIFT)}{spec_char}' \
               f'{key}: ' + '{'
    else:
        return f'{" " * (SPACES_PER_LVL * depth_lvl - LEFT_SHIFT)}{spec_char}' \
               f'{key}: {value}'


def convert_to_json(value):
    if type(value) not in [int, float, dict]:
        return str(value).replace(
            "True", "true").replace(
            "False", "false").replace("None", "null")
    else:
        return value
