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
                lines.append(f'{deep_indent}- {key}: '
                             f'{form_string(old_value, depth_lvl + 1)}')
                lines.append(f'{deep_indent}+ {key}: '
                             f'{form_string(new_value, depth_lvl + 1)}')
            if key_type == 'nested':
                lines.append(f'{deep_indent}  {key}: '
                             f'{inner(value, depth_lvl + 1)}')

            value = f'{form_string(value, depth_lvl + 1)}'
            if key_type == 'unchanged':
                lines.append(f'{deep_indent}  {key}: {value}')
            if key_type == 'deleted':
                lines.append(f'{deep_indent}- {key}: {value}')
            if key_type == 'added':
                lines.append(f'{deep_indent}+ {key}: {value}')

        result = itertools.chain('{', lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner(diff_dict)


def form_string(tree, depth_lvl):

    def inner(node, depth):
        if type(node) != dict:
            if node in [True, False, None]:
                return str(node).lower().replace('none', 'null')
            else:
                return str(node)

        deep_indent = ' ' * SPACES_PER_LVL * depth
        current_indent = ' ' * SPACES_PER_LVL * (depth - 1)
        lines = []
        for key, value in node.items():
            lines.append(f'{deep_indent}{key}: {inner(value, depth + 1)}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner(tree, depth_lvl)
