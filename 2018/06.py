#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict

e = Env(6, [], 10000)
e.T("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""", 17, 16, 32)


def paint_min_dist(grid, coords, min_x, min_y, w, h):
    counters = defaultdict(int)
    for y in range(h):
        vy = y + min_y
        for x in range(w):
            vx = x + min_x
            closest = -1
            best = None
            for i, c in enumerate(coords):
                dist = abs(vx - c[0]) + abs(vy - c[1])
                if best is None or dist < best:
                    closest = i
                    best = dist
                elif dist == best:
                    closest = -1
            grid[y][x] = closest
            if closest != -1:
                counters[closest] += 1
    return counters


def find_infinites(grid, min_x, min_y, w, h):
    inf = set()
    for y in range(h):
        inf.add(grid[y][0])
        inf.add(grid[y][-1])
    for x in range(w):
        inf.add(grid[0][x])
        inf.add(grid[-1][x])
    return inf


def grid_bounds(lines):
    coords = [[int(y) for y in x.split(', ')] for x in lines]
    min_x = min([c[0] for c in coords])
    max_x = max([c[0] for c in coords])
    min_y = min([c[1] for c in coords])
    max_y = max([c[1] for c in coords])
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    return coords, min_x, min_y, w, h


def part1(input):
    coords, min_x, min_y, w, h = grid_bounds(input.get_valid_lines())
    grid = [
        [-1] * w
        for _ in range(h)
    ]
    closest = paint_min_dist(grid, coords, min_x, min_y, w, h)
    inf = find_infinites(grid, min_x, min_y, w, h)

    biggest = None
    count = 0
    for id, cnt in closest.items():
        if id not in inf and (biggest is None or cnt > count):
            biggest = id
            count = cnt
    return count


e.run_tests(1, part1)
e.run_main(1, part1)


def is_safe(x, y, coords, dist_limit):
    dist = sum([
        abs(x - p[0]) + abs(y - p[1])
        for p in coords
    ])
    return dist < dist_limit


def count_safe(dist_limit, coords, min_x, min_y, w, h):
    counter = 0
    for y in range(h):
        vy = y + min_y
        for x in range(w):
            vx = x + min_x
            if is_safe(vx, vy, coords, dist_limit):
                # If any position on the boundary of the grid is safe
                # that means that there might be safe positions also
                # outside the boundary, in which case the result would
                # be wrong
                assert y != 0 and x != 0 and y != h-1 and x != w-1
                counter += 1
    return counter



def part2(input):
    dist_limit = e.get_param()
    coords, min_x, min_y, w, h = grid_bounds(input.get_valid_lines())
    safe_count = count_safe(dist_limit, coords, min_x, min_y, w, h)
    return safe_count


e.run_tests(2, part2)
e.run_main(2, part2)
