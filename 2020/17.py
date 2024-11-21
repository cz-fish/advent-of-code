#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import defaultdict

e = Env(17)
e.T(""".#.
..#
###""", 112, 848)


def make_grid(input):
    ingrid = Grid(input.get_valid_lines())
    grid = defaultdict(bool)
    for row in range(ingrid.h):
        for col in range(ingrid.w):
            if ingrid.grid[row][col] == '#':
                grid[(col, row, 0)] = True
    return grid, ((0, ingrid.w), (0, ingrid.h), (0,1))


def count_neighbors(x, y, z, grid):
    count = 0
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if a == 0 and b == 0 and c == 0:
                    continue
                if (x + a, y + b, z + c) in grid:
                    count += 1
    return count


def game_step(ogrid, olimits):
    grid = defaultdict(bool)
    limits = (
        (olimits[0][0]-1, olimits[0][1]+1),
        (olimits[1][0]-1, olimits[1][1]+1),
        (olimits[2][0]-1, olimits[2][1]+1)
    )
    for x in range(limits[0][0], limits[0][1]):
        for y in range(limits[1][0], limits[1][1]):
            for z in range(limits[2][0], limits[2][1]):
                c = count_neighbors(x, y, z, ogrid)
                a = (x, y, z) in ogrid
                if (a and c in [2,3]) or (not a and c == 3):
                    grid[(x, y, z)] = True
    return grid, limits


def part1(input):
    grid, limits = make_grid(input)
    for turn in range(6):
        grid, limits = game_step(grid, limits)
    return len(grid)


e.run_tests(1, part1)
e.run_main(1, part1)

# Part 2


def count_neighbors_4d(x, y, z, u, grid):
    count = 0
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                for d in [-1, 0, 1]:
                    if a == 0 and b == 0 and c == 0 and d == 0:
                        continue
                    if (x + a, y + b, z + c, u + d) in grid:
                        count += 1
    return count


def grid_to_4d(ogrid, olimits):
    grid = defaultdict(bool)
    limits = (
        olimits[0],
        olimits[1],
        olimits[2],
        (0, 1)
    )
    for x, y, z in ogrid.keys():
        grid[(x, y, z, 0)] = True
    return grid, limits


def game_step_4d(ogrid, olimits):
    grid = defaultdict(bool)
    limits = (
        (olimits[0][0]-1, olimits[0][1]+1),
        (olimits[1][0]-1, olimits[1][1]+1),
        (olimits[2][0]-1, olimits[2][1]+1),
        (olimits[3][0]-1, olimits[3][1]+1)
    )
    for x in range(limits[0][0], limits[0][1]):
        for y in range(limits[1][0], limits[1][1]):
            for z in range(limits[2][0], limits[2][1]):
                for u in range(limits[3][0], limits[3][1]):
                    c = count_neighbors_4d(x, y, z, u, ogrid)
                    a = (x, y, z, u) in ogrid
                    if (a and c in [2,3]) or (not a and c == 3):
                        grid[(x, y, z, u)] = True
    return grid, limits


def part2(input):
    grid, limits = make_grid(input)
    grid, limits = grid_to_4d(grid, limits)
    for turn in range(6):
        grid, limits = game_step_4d(grid, limits)
    return len(grid)


e.run_tests(2, part2)
e.run_main(2, part2)
