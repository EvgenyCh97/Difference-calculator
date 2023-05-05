#!/usr/bin/env python3

from gendiff import generate_diff
from gendiff.parser import parse_args


def main():
    args = parse_args()
    print(generate_diff(args.filepath_1, args.filepath_2, args.format))


if __name__ == '__main__':
    main()
