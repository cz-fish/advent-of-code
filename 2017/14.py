#!/usr/bin/python3.12

from pyaoc import Env
from knot_hash import knot_hash


e = Env(14)
e.T("flqrgnkx", 8108, 1242)


def make_row(hash):
    row = []
    for v in hash:
        for k in [128, 64, 32, 16, 8, 4, 2, 1]:
            row.append('#' if v & k else '.')
    return row


def make_grid(handle):
    grid = []

    for row in range(128):
        key = f"{handle}-{row}"
        hash = knot_hash(key)
        grid.append(make_row(hash))
    
    return grid


def part1(input):
    handles = input.get_lines()
    assert len(handles) == 1
    handle = handles[0]
    grid = make_grid(handle)
    return sum([sum([1 for x in row if x == '#']) for row in grid])


e.run_tests(1, part1)
e.run_main(1, part1)


def explore(grid, r, c, explored):
    explored.add((r, c))
    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nr = r + dr
        nc = c + dc
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[nr]) \
            or grid[nr][nc] != '#' or (nr, nc) in explored:
            continue
        explore(grid, nr, nc, explored)


def count_regions(grid):
    counter = 0
    explored = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '#' and (r, c) not in explored:
                counter += 1
                explore(grid, r, c, explored)
    return counter


def part2(input):
    handles = input.get_lines()
    assert len(handles) == 1
    handle = handles[0]
    grid = make_grid(handle)
    return count_regions(grid)


e.run_tests(2, part2)
e.run_main(2, part2)
