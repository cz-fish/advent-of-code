#!/usr/bin/python3.12

from pyaoc import Env, Grid

e = Env(6)
e.T("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""", 41, 6)


def find_start(grid):
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.get(row, col) == '^':
                return row, col
    assert False, "No starting position in grid"


def part1(input):
    g = Grid(input.get_valid_lines())
    row, col = find_start(g)
    visited = set()
    visited.add((row, col))
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    curdir = 0
    while True:
        step = dirs[curdir]
        newrow = row + step[0]
        newcol = col + step[1]
        if not g.is_in(newrow, newcol):
            #print(f"Left grid at {row} {col} direction {step}")
            break
        if g.get(newrow, newcol) != '#':
            row = newrow
            col = newcol
            visited.add((row, col))
        else:
            curdir = (curdir + 1) % 4
            #print(f"Turning at position {row} {col} from {step} to {dirs[curdir]}")
    return len(visited)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
