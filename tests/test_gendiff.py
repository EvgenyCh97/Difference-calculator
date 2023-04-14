import json
import pytest
from gendiff import stylish, gendiff

JSON1 = 'tests/fixtures/file3.json'
JSON2 = 'tests/fixtures/file4.json'
YAML1 = 'tests/fixtures/file1.yaml'
YAML2 = 'tests/fixtures/file2.yml'


def test_get_dict_from_():
    result = gendiff.get_dict_from_(JSON1)
    assert result == {'common': {
        'setting1': 'Value 1',
        'setting2': 200,
        'setting3': True,
        'setting6':
            {'key': 'value', 'doge': {'wow': ''}}},
        'group1': {'baz': 'bas', 'foo': 'bar',
                   'nest': {'key': 'value'}},
        'group2': {'abc': 12345, 'deep': {'id': 45}}}

    result = gendiff.get_dict_from_(JSON2)
    assert result == {'common': {
        'follow': False,
        'setting1': 'Value 1',
        'setting3': None,
        'setting4': 'blah blah',
        'setting5': {'key5': 'value5'},
        'setting6': {
            'key': 'value', 'ops': 'vops', 'doge': {'wow': 'so much'}}},
        'group1': {'foo': 'bar', 'baz': 'bars', 'nest': 'str'},
        'group3': {'deep': {'id': {'number': 45}}, 'fee': 100500}}

    result = gendiff.get_dict_from_(YAML1)
    assert result == {'host': 'hexlet.io', 'timeout': 50,
                      'proxy': '123.234.53.22', 'follow': False}

    result = gendiff.get_dict_from_(YAML2)
    assert result == {'timeout': 20, 'verbose': True, 'host': 'hexlet.io'}


def test_convert_bool_and_null_to_str():
    result = gendiff.convert_bool_and_null_to_str({'common': {
        'setting1': False,
        'setting2': None,
        'setting3': True,
        'setting6': {
            'key': 'value',
            'doge': {
                'wow': ''}}}})
    assert result == {'common': {
        'setting1': 'false', 'setting2': 'null', 'setting3': 'true',
        'setting6': {'key': 'value', 'doge': {'wow': ''}}}}


def test_get_stylish():
    result = stylish.get_stylish({
        'group1': {
            'type': 'added', 'value': {
                'foo': {'type': 'unchanged', 'value': 'bar', 'depth': 2},
                'baz': {'type': 'unchanged', 'value': 'bars', 'depth': 2},
                'nest': {'type': 'unchanged', 'value': 'str', 'depth': 2}},
            'depth': 1}})
    assert result == ['  + group1: {', '        baz: bars',
                      '        foo: bar', '        nest: str', '    }', '}']


def test_compare_files():
    compare = gendiff.compare_files()
    result = compare(
        {'group1': {'baz': 'bas', 'foo': 'bar', 'nest': {'key': 'value'}}},
        {'group1': {'foo': 'bar', 'baz': 'bars', 'nest': 'str'}})
    assert result == {'group1': {
        'type': 'nested', 'value': {
            'baz': {'type': 'changed',
                    'value': 'bars', 'old_value': 'bas', 'depth': 2},
            'foo': {'type': 'unchanged', 'value': 'bar', 'depth': 2},
            'nest': {'type': 'changed',
                     'value': 'str',
                     'old_value': {
                         'key': {'type': 'unchanged',
                                 'value': 'value', 'depth': 3}},
                     'depth': 2}},
        'depth': 1}}

    result = compare(
        {'host': 'hexlet.io', 'timeout': 50,
         'proxy': '123.234.53.22', 'follow': 'false'},
        {'timeout': 20, 'verbose': 'true', 'host': 'hexlet.io'})
    assert result == {
        'host': {'type': 'unchanged', 'value': 'hexlet.io', 'depth': 1},
        'timeout': {'type': 'changed', 'value': 20, 'old_value': 50,
                    'depth': 1},
        'proxy': {'type': 'deleted', 'value': '123.234.53.22', 'depth': 1},
        'follow': {'type': 'deleted', 'value': 'false', 'depth': 1},
        'verbose': {'type': 'added', 'value': 'true', 'depth': 1}}


def test_generate_diff():
    result = gendiff.generate_diff(JSON1, JSON2)
    with open('tests/fixtures/json_diff', 'r') as json_diff:
        assert result == json_diff.read()

    result = gendiff.generate_diff(YAML1, YAML2)
    with open('tests/fixtures/yaml_diff', 'r') as yaml_diff:
        assert result == yaml_diff.read()
