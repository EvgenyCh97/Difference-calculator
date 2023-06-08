import itertools

SPACES_PER_LVL = 4
LEFT_SHIFT = 2


def get_stylish(diff_dict):

    def inner(node, depth_lvl=1):
        deep_indent = ' ' * (SPACES_PER_LVL * depth_lvl - LEFT_SHIFT)
        current_indent = ' ' * SPACES_PER_LVL * (depth_lvl - 1)
        lines = []
        sorted_keys = sorted(node)
        for key in sorted_keys:
            key_type = node[key].get('type')
            value = node.get(key).get('value')
            if key_type == 'changed':
                old_value = node[key]['old_value']
                new_value = node[key]['new_value']
                lines.append(f'{deep_indent}- {key}: {form_string(old_value, depth_lvl + 1)}')
                lines.append(f'{deep_indent}+ {key}: {form_string(new_value, depth_lvl + 1)}')
            if key_type == 'nested':
                lines.append(f'{deep_indent}  {key}: {inner(value, depth_lvl + 1)}')
            if key_type == 'unchanged':
                lines.append(f'{deep_indent}  {key}: {form_string(value, depth_lvl + 1)}')
            if key_type == 'deleted':
                lines.append(f'{deep_indent}- {key}: {form_string(value, depth_lvl + 1)}')
            if key_type == 'added':
                lines.append(f'{deep_indent}+ {key}: {form_string(value, depth_lvl + 1)}')

        result = itertools.chain('{', lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner(diff_dict)


def form_string(value, depth_lvl):

    def inner(current_value, depth):
        if type(current_value) != dict:
            if current_value in [True, False, None]:
                return str(current_value).lower().replace('none', 'null')
            else:
                return str(current_value)

        deep_indent = ' ' * SPACES_PER_LVL * depth
        current_indent = ' ' * SPACES_PER_LVL * (depth - 1)
        lines = []
        for key, val in current_value.items():
            lines.append(f'{deep_indent}{key}: {inner(val, depth + 1)}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner(value, depth_lvl)
