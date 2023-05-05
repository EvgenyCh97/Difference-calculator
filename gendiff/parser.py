import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('filepath_1', type=str, help='path to first file')
    parser.add_argument('filepath_2', type=str, help='path to second file')
    parser.add_argument('-f', '--format', type=str, metavar='',
                        default='stylish',
                        help='set format of output (default: "stylish")')
    args = parser.parse_args()
    return args
