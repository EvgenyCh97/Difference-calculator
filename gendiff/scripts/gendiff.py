#!/usr/bin/env python3

from gendiff import generate_diff
from gendiff.parser import ARGS


def main():
    print(generate_diff(ARGS.filepath_1, ARGS.filepath_2, ARGS.format))


if __name__ == '__main__':
    main()
