#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque

def eT(*a): pass

e = Env(12)
e.T("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", 1930, 1206)

e.T("""AAAA
BBCD
BBCC
EEEC""", 140, 80)

e.T("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""", None, 236)

e.T("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""", None, 368)

e.T("""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""", None, 436)


def add_region(g, row, col, visited):
    kind = g.get(row, col)
    area = 0
    horizontal_border = set()
    vertical_border = set()
    q = deque()
    q.append((row, col))
    while q:
        r, c = q.popleft()
        if (r, c) in visited:
            continue
        area += 1
        visited.add((r, c))
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr = r + dr
            nc = c + dc
            if not g.is_in(nr, nc) or g.get(nr, nc) != kind:
                if nr == r:
                    vertical_border.add((r, c, nc))
                else:
                    horizontal_border.add((c, r, nr))
            elif (nr, nc) not in visited:
                q.append((nr, nc))
    circ = len(horizontal_border) + len(vertical_border)
    # count edges
    edges = 0
    while horizontal_border:
        c, r1, r2 = horizontal_border.pop()
        x = c - 1
        while (x, r1, r2) in horizontal_border:
            horizontal_border.remove((x, r1, r2))
            x -= 1
        x = c + 1
        while (x, r1, r2) in horizontal_border:
            horizontal_border.remove((x, r1, r2))
            x += 1
        edges += 1
    while vertical_border:
        r, c1, c2 = vertical_border.pop()
        x = r - 1
        while (x, c1, c2) in vertical_border:
            vertical_border.remove((x, c1, c2))
            x -= 1
        x = r + 1
        while (x, c1, c2) in vertical_border:
            vertical_border.remove((x, c1, c2))
            x += 1
        edges += 1
    return area, circ, edges


def find_regions(g):
    regions = []
    visited = set()
    for row in range(g.h):
        for col in range(g.w):
            if (row, col) in visited:
                continue
            regions.append(add_region(g, row, col, visited))
    return regions


def part1(input):
    g = Grid(input.get_valid_lines())
    regions = find_regions(g)
    return sum([a * c for a, c, _ in regions])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines())
    regions = find_regions(g)
    return sum([a * e for a, _, e in regions])


e.run_tests(2, part2)
e.run_main(2, part2)
