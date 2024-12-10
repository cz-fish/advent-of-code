#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque

e = Env(10)
e.T("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", 36, 81)


def score(g, start_r, start_c):
    peaks = set()
    rating = 0
    q = deque()
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    q.append((start_r, start_c, 0))
    while q:
        r, c, val = q.popleft()
        if val == 9:
            peaks.add((r, c))
            rating += 1
        else:
            for dr, dc in dirs:
                nr = r + dr
                nc = c + dc
                if g.is_in(nr, nc) and g.get(nr, nc) == val + 1:
                    q.append((nr, nc, val + 1))
    return len(peaks), rating


def solve(g):
    total_score = 0
    total_rating = 0
    for r in range(g.h):
        for c in range(g.w):
            if g.get(r, c) == 0:
                sc, rat = score(g, r, c)
                total_score += sc
                total_rating += rat
    return total_score, total_rating


def part1(input):
    g = Grid(input.get_valid_lines(), ints=True)
    return solve(g)[0]


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines(), ints=True)
    return solve(g)[1]


e.run_tests(2, part2)
e.run_main(2, part2)
