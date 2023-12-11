#!/usr/bin/python3.8

from aoc import Env, Grid
e = Env(11, param=1000000)
e.T("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 374, 1030, param=10)
e.T("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", None, 8410, param=100)


def find_galaxies(grid):
    gal = []
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.get(row, col) == '#':
                gal.append((row, col))
    return gal


def galaxy_distance(first, second, exp_rows, exp_cols, mult):
    mr = min(first[0], second[0])
    Mr = max(first[0], second[0])
    mc = min(first[1], second[1])
    Mc = max(first[1], second[1])
    dist = Mr-mr + Mc-mc
    for dr in exp_rows:
        if mr < dr and dr < Mr:
            dist += mult
        elif dr > Mr:
            break
    for dc in exp_cols:
        if mc < dc and dc < Mc:
            dist += mult
        elif dc > Mc:
            break
    return dist


def solve(input, multiplier):
    grid = Grid(input.get_valid_lines())
    gal = find_galaxies(grid)
    used_rows = set([r for r, _ in gal])
    used_cols = set([c for _, c in gal])
    expanded_rows = [r for r in range(grid.h) if r not in used_rows]
    expanded_cols = [c for c in range(grid.w) if c not in used_cols]

    distances = 0
    for g, first in enumerate(gal):
        for second in gal[g+1:]:
            distances += galaxy_distance(first, second, expanded_rows, expanded_cols, multiplier - 1)
    return distances


def part1(input):
    return solve(input, 2)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return solve(input, e.get_param())


e.run_tests(2, part2)
e.run_main(2, part2)
