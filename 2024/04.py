#!/usr/bin/python3.12

from pyaoc import Env, Grid
import re

e = Env(4)
e.T("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""", 18, 9)


def check_xmas(g, row, col, dr, dc):
    er = row + 3 * dr
    ec = col + 3 * dc
    if not g.is_in(er, ec):
        return 0
    s = g.get(row, col) + g.get(row+dr, col+dc) + g.get(row+2*dr, col+2*dc) + g.get(row+3*dr, col+3*dc)
    return 1 if s == "XMAS" else 0


def count_xmas(g):
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]
    total = 0
    for row in range(g.h):
        for col in range(g.w):
            for dr, dc in directions:
                total += check_xmas(g, row, col, dr, dc)
    return total


def part1(input):
    g = Grid(input.get_valid_lines())
    return count_xmas(g)


e.run_tests(1, part1)
e.run_main(1, part1)


def count_x_shaped_mas(g):
    total = 0
    for row in range(1, g.h-1):
        for col in range(1, g.w-1):
            if g.get(row, col) != 'A':
                continue
            diag = g.get(row-1, col-1) + g.get(row, col) + g.get(row+1, col+1)
            if diag != "MAS" and diag != "SAM":
                continue
            diag = g.get(row-1, col+1) + g.get(row, col) + g.get(row+1, col-1)
            if diag != "MAS" and diag != "SAM":
                continue
            total += 1
    return total


def part2(input):
    g = Grid(input.get_valid_lines())
    return count_x_shaped_mas(g)


e.run_tests(2, part2)
e.run_main(2, part2)
