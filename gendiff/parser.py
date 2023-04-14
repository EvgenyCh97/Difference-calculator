import argparse

parser = argparse.ArgumentParser(
    description='Compares two configuration files and shows a difference.'
)
parser.add_argument('filepath_1', type=str, help='path to first file')
parser.add_argument('filepath_2', type=str, help='path to second file')
parser.add_argument('-f', '--format [type]', metavar='',
                    help='set format of output (default: "stylish")')

ARGS = parser.parse_args()
