import pytest
import json
from gendiff import gendiff

JSON1 = 'tests/fixtures/file1.json'
JSON2 = 'tests/fixtures/file2.json'


@pytest.fixture
def json_dict1():
    return json.load(open(JSON1))


@pytest.fixture
def json_dict2():
    return json.load(open(JSON2))


def test_get_dicts_from_():
    result = gendiff.get_dicts_from_(JSON1,
                                     JSON2)
    assert result == ({'host': 'hexlet.io', 'timeout': 50,
                       'proxy': '123.234.53.22', 'follow': False, '123': 1},
                      {'timeout': 20, 'verbose': True, 'host': 'hexlet.io',
                       '123': 2}
                      )
    result = gendiff.get_dicts_from_('tests/fixtures/file1.yaml',
                                     'tests/fixtures/file2.yml')
    assert result == ({'a': 1, 'b': None, 'c': 3, 'd': 4},
                      {'a': 1, 'b': None, 'c': 5, 'd': 7})


def test_get_items_list(json_dict1, json_dict2):
    result1 = gendiff.get_items_list(json_dict1)
    result2 = gendiff.get_items_list(json_dict2)
    assert result1 == [('host', 'hexlet.io'), ('timeout', 50),
                       ('proxy', '123.234.53.22'), ('follow', False),
                       ('123', 1)
                       ]
    assert result2 == [('timeout', 20), ('verbose', True),
                       ('host', 'hexlet.io'), ('123', 2)
                       ]


def test_get_keys_set_from_(json_dict1, json_dict2):
    result = gendiff.get_keys_set_from_(json_dict1, json_dict2)
    assert result == ({'proxy', '123', 'timeout', 'follow', 'host'},
                      {'timeout', '123', 'verbose', 'host'}
                      )


def test_encode_(json_dict1, json_dict2):
    result1 = gendiff.encode_(json_dict1)
    result2 = gendiff.encode_(json_dict2)
    with open(JSON1, 'r') as json_file1:
        assert result1 == json_file1.read()
    with open(JSON2, 'r') as json_file2:
        assert result2 == json_file2.read()


def test_sort_():
    result = gendiff.sort_([('  b', 'second'), ('  a', 'first')])
    assert result == [('  a', 'first'), ('  b', 'second')]


def test_get_matches():
    result = gendiff.get_matches(JSON1, JSON2)
    assert set(result) == {('  host', 'hexlet.io')}


def test_get_new_lines():
    result = gendiff.get_new_lines(JSON1, JSON2)
    assert set(result) == {('+ verbose', True)}


def test_get_old_lines():
    result = gendiff.get_old_lines(JSON1, JSON2)
    assert set(result) == {('- proxy', '123.234.53.22'), ('- follow', False)}


def test_get_updated_lines():
    result = gendiff.get_updated_lines(JSON1, JSON2)
    assert set(result[0]) == {('- timeout', 50), ('- 123', 1)}
    assert set(result[1]) == {('+ timeout', 20), ('+ 123', 2)}


def test_get_result_list():
    result = gendiff.get_result_list(JSON1, JSON2,
                                     gendiff.get_matches,
                                     gendiff.get_new_lines,
                                     gendiff.get_old_lines,
                                     gendiff.get_updated_lines
                                     )
    assert set(result) == {('  host', 'hexlet.io'), ('+ verbose', True),
                           ('- proxy', '123.234.53.22'), ('- follow', False),
                           ('- timeout', 50), ('- 123', 1), ('+ timeout', 20),
                           ('+ 123', 2)}


def test_generate_diff():
    result = gendiff.generate_diff(JSON1, JSON2)
    with open('tests/fixtures/diff', 'r') as diff:
        assert result == diff.read()
