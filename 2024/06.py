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

e.T("""##..
^..#
....
..#.""", 6, 1)

e.T(""".#.
.^#
...
.#.""", 3, 1)

e.T("""....
#^.#
..#.""", 2, 1)


def find_start(grid):
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.get(row, col) == '^':
                return row, col
    assert False, "No starting position in grid"


k_dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def next_dir(cur_dir):
    return (cur_dir + 1) % 4


def walk_visit(g, row, col, curdir, ignore_visited=False):
    """
    Return (loop, visited)
        - loop is true if the walk results in a loop; false if escaped
        - visited is set of all visited places
    """
    visited = set()
    while True:
        if (row, col, curdir) in visited:
            # looped
            if ignore_visited:
                return (True, None)
            else:
                return (True, set([(row, col) for row, col, _ in visited]))
        visited.add((row, col, curdir))
        step = k_dirs[curdir]
        newrow = row + step[0]
        newcol = col + step[1]
        if not g.is_in(newrow, newcol):
            # escape grid
            if ignore_visited:
                return (False, None)
            else:
                return (False, set([(row, col) for row, col, _ in visited]))
        ahead = g.get(newrow, newcol)
        if ahead != '#':
            # move ahead on our path
            row = newrow
            col = newcol
        else:
            # obstacle ahead. Turn
            curdir = next_dir(curdir)


def part1(input):
    g = Grid(input.get_valid_lines())
    row, col = find_start(g)
    curdir = 0
    looped, visited = walk_visit(g, row, col, curdir)
    assert not looped
    return len(visited)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines())
    row, col = find_start(g)
    curdir = 0
    looped, visited = walk_visit(g, row, col, curdir, ignore_visited=False)
    assert not looped
    obstacles = 0
    for rvis, cvis in visited:
        if rvis == row and cvis == col:
            continue
        g.grid[rvis][cvis] = '#'
        looped, _ = walk_visit(g, row, col, curdir, ignore_visited=True)
        if looped:
            obstacles += 1
        g.grid[rvis][cvis] = '.'
    return obstacles


e.run_tests(2, part2)
e.run_main(2, part2)
