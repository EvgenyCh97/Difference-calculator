#!/usr/bin/env python3

from gendiff.parser import ARGS
from gendiff.gendiff import generate_diff


def main():
    print(generate_diff(ARGS.filepath_1, ARGS.filepath_2))


if __name__ == '__main__':
    main()
