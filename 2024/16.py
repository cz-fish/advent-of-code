#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque

e = Env(16)
e.T("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 7036, 45)

e.T("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""", 11048, 64)


def find_position(g, which_one):
    for row in range(g.h):
        for col in range(g.w):
            if g.get(row, col) == which_one:
                return row, col
    assert False, f"Position {which_one} not found"


def shortest_dfs(g, start, end):
    min_dists = {}
    q = deque()
    # E = 0, N = 1, W = 2, S = 3
    facing = 0
    steps = {
        0: (0, 1),
        1: (-1, 0),
        2: (0, -1),
        3: (1, 0)
    }
    q.append((start[0], start[1], facing, 0))
    while q:
        r, c, facing, score = q.pop()
        coords = (r, c, facing)
        if coords in min_dists and min_dists[coords] <= score:
            continue
        min_dists[coords] = score
        if coords == end:
            # no need to search any further from end
            continue
        # first turn around
        nscore = score + 1000
        q.append((r, c, (facing + 1) % 4, nscore))
        q.append((r, c, (facing - 1) % 4, nscore))
        # then continue in the same direction
        dr, dc = steps[facing]
        nr = r + dr
        nc = c + dc
        nfacing = facing
        nscore = score + 1
        if g.get(nr, nc) != '#':
            if (nr, nc, nfacing) not in min_dists or min_dists[(nr, nc, nfacing)] > nscore:
                q.append((nr, nc, nfacing, nscore))
    best = None
    for facing in range(4):
        coord = (end[0], end[1], facing)
        if coord not in min_dists:
            continue
        val = min_dists[coord]
        if best is None or val < best:
            best = val
    assert best is not None, f"Path to end {end} not found"
    return best



def part1(input):
    g = Grid(input.get_valid_lines())
    start = find_position(g, 'S')
    end = find_position(g, 'E')
    return shortest_dfs(g, start, end)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
