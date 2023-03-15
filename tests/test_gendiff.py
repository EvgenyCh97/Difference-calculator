import pytest
import json
from gendiff import gendiff

JSON1 = 'tests/fixtures/file1.json'
JSON2 = 'tests/fixtures/file2.json'
YAML1 = 'tests/fixtures/file1.yaml'
YAML2 = 'tests/fixtures/file2.yml'


@pytest.fixture
def json_dict1():
    return json.load(open(JSON1))


@pytest.fixture
def json_dict2():
    return json.load(open(JSON2))


def test_get_dict_from_():
    result = gendiff.get_dict_from_(JSON1)
    assert result == ({'host': 'hexlet.io', 'timeout': 50,
                       'proxy': '123.234.53.22', 'follow': False})

    result = gendiff.get_dict_from_(JSON2)
    assert result == ({'timeout': 20, 'verbose': True, 'host': 'hexlet.io'})

    result = gendiff.get_dict_from_(YAML1)
    assert result == ({'host': 'hexlet.io', 'timeout': 50,
                       'proxy': '123.234.53.22', 'follow': False})

    result = gendiff.get_dict_from_(YAML2)
    assert result == ({'timeout': 20, 'verbose': True, 'host': 'hexlet.io'})


def test_encode_(json_dict1, json_dict2):
    result = gendiff.encode_(json_dict1)
    with open(JSON1, 'r') as json_file1:
        assert result == json_file1.read()

    result = gendiff.encode_(json_dict2)
    with open(JSON2, 'r') as json_file2:
        assert result == json_file2.read()


def test_sort_():
    result = gendiff.sort_([('  b', 'second'), ('  a', 'first')])
    assert result == [('  a', 'first'), ('  b', 'second')]


def test_generate_diff():
    result = gendiff.generate_diff(JSON1, JSON2)
    with open('tests/fixtures/diff', 'r') as diff:
        assert result == diff.read()

    result = gendiff.generate_diff(YAML1, YAML2)
    with open('tests/fixtures/diff', 'r') as diff:
        assert result == diff.read()
