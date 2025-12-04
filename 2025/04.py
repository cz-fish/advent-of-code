#!/usr/bin/python3.12

from pyaoc import Env, Grid


e = Env(4)
e.T("""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""", 13, 43)


def can_remove(g, row, col):
    if g.get(row, col) != '@':
        return False
    nei = sum([1 for y, x in g.neighbors8(row, col) if g.get(y, x) == '@'])
    return nei < 4


def part1(input):
    g = Grid(input.get_valid_lines())
    total = 0
    for row in range(g.h):
        for col in range(g.w):
            if can_remove(g, row, col):
                total += 1
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines())
    all_rolls = set()
    removals = set()
    for row in range(g.h):
        for col in range(g.w):
            if g.get(row, col) != '@':
                continue
            all_rolls.add((row, col))
            if can_remove(g, row, col):
                removals.add((row, col))
    total = len(removals)
    while removals:
        candidates = set()
        for row, col in removals:
            g.grid[row][col] = '.'
            for nei in g.neighbors8(row, col):
                if nei in all_rolls and nei not in removals:
                    candidates.add(nei)
        removals.clear()
        for row, col in candidates:
            if can_remove(g, row, col):
                removals.add((row, col))
        total += len(removals)
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
