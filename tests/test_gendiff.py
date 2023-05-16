from gendiff import gendiff

JSON1 = 'tests/fixtures/file1.json'
JSON2 = 'tests/fixtures/file2.json'
YAML1 = 'tests/fixtures/file1.yaml'
YAML2 = 'tests/fixtures/file2.yml'


def test_get_dict_from():
    result = gendiff.get_dict_from(JSON1)
    assert result == {'common': {
        'setting1': 'Value 1',
        'setting2': 200,
        'setting3': True,
        'setting6':
            {'key': 'value', 'doge': {'wow': ''}}},
        'group1': {'baz': 'bas', 'foo': 'bar',
                   'nest': {'key': 'value'}},
        'group2': {'abc': 12345, 'deep': {'id': 45}}}

    result = gendiff.get_dict_from(JSON2)
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

    result = gendiff.get_dict_from(YAML1)
    assert result == {'host': 'hexlet.io', 'timeout': 50,
                      'proxy': '123.234.53.22', 'follow': False}

    result = gendiff.get_dict_from(YAML2)
    assert result == {'timeout': 20, 'verbose': True, 'host': 'hexlet.io'}


def test_get_diff_dict():
    result = gendiff.get_diff_dict(
        {'group1': {'baz': 'bas', 'foo': 'bar', 'nest': {'key': 'value'}}},
        {'group1': {'foo': 'bar', 'baz': 'bars', 'nest': 'str'}})
    assert result == {'group1': {
        'type': 'nested', 'value': {
            'baz': {'type': 'changed',
                    'value': 'bars', 'old_value': 'bas'},
            'foo': {'type': 'unchanged', 'value': 'bar'},
            'nest': {'type': 'changed',
                     'value': 'str',
                     'old_value': {
                         'key': {'type': 'unchanged',
                                 'value': 'value'}}}}}}

    result = gendiff.get_diff_dict(
        {'host': 'hexlet.io', 'timeout': 50,
         'proxy': '123.234.53.22', 'follow': 'false'},
        {'timeout': 20, 'verbose': 'true', 'host': 'hexlet.io'})
    assert result == {
        'host': {'type': 'unchanged', 'value': 'hexlet.io'},
        'timeout': {'type': 'changed', 'value': 20, 'old_value': 50},
        'proxy': {'type': 'deleted', 'value': '123.234.53.22'},
        'follow': {'type': 'deleted', 'value': 'false'},
        'verbose': {'type': 'added', 'value': 'true'}}


def test_generate_diff():
    result = gendiff.generate_diff(JSON1, JSON2)
    with open('tests/fixtures/diff', 'r') as diff:
        assert result == diff.read()

    result = gendiff.generate_diff(YAML1, YAML2)
    with open('tests/fixtures/yaml_diff', 'r') as yaml_diff:
        assert result == yaml_diff.read()

    result = gendiff.generate_diff(JSON1, JSON2, format_name='plain')
    with open('tests/fixtures/plain_diff', 'r') as plain_diff:
        assert result == plain_diff.read()

    result = gendiff.generate_diff(JSON1, JSON2, format_name='json')
    with open('tests/fixtures/json_diff', 'r') as json_diff:
        assert result == json_diff.read()
