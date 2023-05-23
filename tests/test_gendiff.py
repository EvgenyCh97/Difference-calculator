import pytest
from gendiff import gendiff

JSON1 = 'tests/fixtures/file1.json'
JSON2 = 'tests/fixtures/file2.json'
YAML1 = 'tests/fixtures/file1.yaml'
YAML2 = 'tests/fixtures/file2.yml'


@pytest.mark.parametrize(
    "filepath1, filepath2, format, expected",
    [(JSON1, JSON2, 'stylish', 'tests/fixtures/diff'),
     (YAML1, YAML2, 'stylish', 'tests/fixtures/yaml_diff'),
     (JSON1, JSON2, 'plain', 'tests/fixtures/plain_diff'),
     (JSON1, JSON2, 'json', 'tests/fixtures/json_diff')])
def test_generate_diff(filepath1, filepath2, format, expected):
    with open(expected, 'r') as diff:
        assert gendiff.generate_diff(
            filepath1, filepath2, format) == diff.read()
