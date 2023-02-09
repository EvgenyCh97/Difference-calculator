#!/usr/bin/env pethon3

from gendiff.parser import ARGS
from gendiff.gendiff import generate_diff


def main():
    print(generate_diff(ARGS.first_file, ARGS.second_file))


if __name__ == '__main__':
    main()
