#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import deque

e = Env(12)
e.T("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""", 31, 29)


def height(c):
    if c == 'S':
        c = 'a'
    elif c == 'E':
        c = 'z'
    assert c >= 'a' and c <= 'z'
    return ord(c) - ord('a')


def find_start(grid, start_symbol):
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.grid[row][col] == start_symbol:
                return row, col
    assert False, "no S in input"


def find_E(grid, start, goal, reverse_walk):
    q = deque()
    vis = set()
    q.append((start[0], start[1], 0, height(grid.get(start[0], start[1]))))
    while q:
        row, col, dist, elev = q.popleft()
        if (row, col) in vis:
            continue
        vis.add((row, col))
        c = grid.grid[row][col]
        if c == goal:
            return dist
        for r, c in grid.neighbors4(row, col):
            if (r, c) in vis:
                continue
            h = height(grid.get(r, c))
            can_step = (h >= elev - 1) if reverse_walk else (h <= elev + 1)
            if can_step:
                q.append((r, c, dist + 1, h))
    assert False, f"'{goal}' not found"



def part1(input):
    grid = Grid(input.get_valid_lines())
    start = find_start(grid, 'S')
    return find_E(grid, start, 'E', False)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    grid = Grid(input.get_valid_lines())
    start = find_start(grid, 'E')
    return find_E(grid, start, 'a', True)


e.run_tests(2, part2)
e.run_main(2, part2)
