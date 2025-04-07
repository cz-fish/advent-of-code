#!/usr/bin/python3.12

from pyaoc import Env

e = Env(25)
e.T("row 1, column 1.", 20151125, None)
e.T("row 2, column 1.", 31916031, None)
e.T("row 3, column 3.", 1601130, None)
e.T("row 6, column 6.", 27995004, None)


seed = 20151125
mult = 252533
rem = 33554393


def triangle_index(coords):
    row, col = coords
    diag = row + col - 1
    offset = (diag - 1) * diag // 2
    return offset + col - 1


def code_at_index(index):
    v = seed
    for _ in range(index):
        v = (v * mult) % rem
    return v


def part1(input):
    coords = input.get_all_ints()
    index = triangle_index(coords)
    return code_at_index(index)


e.run_tests(1, part1)
e.run_main(1, part1)
