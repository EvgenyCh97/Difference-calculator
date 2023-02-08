import argparse
import json

parser = argparse.ArgumentParser(
    description='Compares two configuration files and shows a difference.'
)
parser.add_argument('first_file', type=str)
parser.add_argument('second_file', type=str)
parser.add_argument('-f', '--format', help='set format of output')
arguments = parser.parse_args()


def get_dicts_from_(file_path1, file_path2):
    return json.load(open(file_path1)), json.load(open(file_path2))


def get_items_list(dictionary):
    return list(dictionary.items())


def get_keys_set_from_(dict1, dict2):
    return ({items[0] for items in get_items_list(dict1)},
            {items[0] for items in get_items_list(dict2)})


def encode_(encoded_list):
    return json.dumps(dict(encoded_list), sort_keys=False, indent=2)


def sort_(sortable_list):
    return sorted(sortable_list, key=lambda items: items[0][2])


def get_matches(file_path1, file_path2):
    dict1, dict2 = get_dicts_from_(file_path1, file_path2)
    set1 = set(get_items_list(dict1))
    set2 = set(get_items_list(dict2))
    set1.intersection_update(set2)
    return [(f'  {key}', dict1.get(key))
            for key in [items[0]
                        for items in set1]]


def get_new_lines(file_path1, file_path2):
    dict1, dict2 = get_dicts_from_(file_path1, file_path2)
    set1, set2 = get_keys_set_from_(dict1, dict2)
    set2.difference_update(set1)
    return [(f'+ {key}', dict2.get(key)) for key in set2]


def get_old_lines(file_path1, file_path2):
    dict1, dict2 = get_dicts_from_(file_path1, file_path2)
    set1, set2 = get_keys_set_from_(dict1, dict2)
    set1.difference_update(set2)
    return [(f'- {key}', dict1.get(key)) for key in set1]


def get_updated_lines(file_path1, file_path2):
    dict1, dict2 = get_dicts_from_(file_path1, file_path2)
    set1, set2 = get_keys_set_from_(dict1, dict2)
    set1.intersection_update(set2)
    diff1, diff2 = dict(), dict()
    for key in set1:
        if dict1[key] != dict2[key]:
            diff1[f'- {key}'] = dict1.get(key)
            diff2[f'+ {key}'] = dict2.get(key)
    result = list()
    result.append(get_items_list(diff1))
    result.append(get_items_list(diff2))
    return result


def get_result_list(file_path1, file_path2, *args):
    result = list()
    for element in [func(file_path1, file_path2) for func in args]:
        if type(element[0]) == tuple:
            for items_tuple in element:
                result.append(items_tuple)
        if type(element[0]) == list:
            for items_list in element:
                for item in items_list:
                    result.append(item)
    return result


def generate_diff():
    return encode_(sort_(get_result_list(
        arguments.first_file,
        arguments.second_file,
        get_matches,
        get_new_lines,
        get_old_lines,
        get_updated_lines))).replace('"', '').replace(',', '')
