#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import deque

e = Env(11)
e.T("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""", 1656, 195)


def step(grid):
    update = deque()
    flashed = set()

    def light(r, c):
        grid.grid[r][c] += 1
        if grid.grid[r][c] > 9:
            grid.grid[r][c] = 0
            flashed.add((r, c))
            update.extend(grid.neighbors8(r, c))

    for row in range(grid.h):
        for col in range(grid.w):
            light(row, col)
    while update:
        row, col = update.popleft()
        if (row, col) not in flashed:
            light(row, col)

    return len(flashed)


def print_grid(step, flashes, grid):
    print(f"Step {step}, flashes {flashes}")
    for ln in grid.grid:
        print("".join([str(x) for x in ln]))
    print("")


def part1(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    flashes = 0
    for i in range(100):
        flashes += step(grid)
        #print_grid(i+1, flashes, grid)
    return flashes


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    i = 0
    while True:
        i += 1
        flashes = step(grid)
        if flashes == 100:
            return i
        if i % 1000 == 0:
            print(i)

e.run_tests(2, part2)
e.run_main(2, part2)

