#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import defaultdict, deque

e = Env(7)
e.T(""".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""", 21, 40)


def find_splitters(g):
    start = None
    splitters = defaultdict(list)
    for row in range(g.h):
        for col in range(g.w):
            c = g.get(row, col)
            if c == 'S':
                assert start is None
                #assert row == 0
                start = (row, col)
            elif c == '^':
                splitters[col].append(row)
    assert start is not None
    return start, splitters


def part1(input):
    g = Grid(input.get_valid_lines())
    start, splitters = find_splitters(g)
    #print(start, list(splitters.keys()))
    activated = set()
    q = deque([start])
    while q:
        row, col = q.popleft()
        if col not in splitters:
            continue
        for s in splitters[col]:
            assert s != row
            if s > row:
                if (s, col) in activated:
                    break
                activated.add((s, col))
                if col > 0:
                    q.append((s, col - 1))
                if col < g.w - 1:
                    q.append((s, col + 1))
                break
    return len(activated)


e.run_tests(1, part1)
e.run_main(1, part1)


def timelines_from_pos(row, col, timelines, splitters):
    if (row, col) in timelines:
        return timelines[(row, col)]
    row_lower_limit = 0
    # Find the nearest splitter above current position in the same
    # column.
    for s in splitters[col]:
        if s >= row:
            break
        row_lower_limit = s
    # Find all splitters in adjacent columns to the left and to the
    # right that are on rows between (row_limit, row). Those are
    # the only ones that can contribute.
    total = 0
    for s in splitters[col - 1]:
        if s >= row:
            break
        if s > row_lower_limit:
            total += timelines_from_pos(s, col - 1, timelines, splitters)
    for s in splitters[col + 1]:
        if s >= row:
            break
        if s > row_lower_limit:
            total += timelines_from_pos(s, col + 1, timelines, splitters)
    timelines[(row, col)] = total
    return total


def part2(input):
    g = Grid(input.get_valid_lines())
    start, splitters = find_splitters(g)
    topmost_splitter = splitters[start[1]][0]
    # one tachyon reaches topmost splitter, the one under S
    timelines = {(topmost_splitter, start[1]): 1}
    total = 0
    for col in range(g.w):
        total += timelines_from_pos(g.h - 1, col, timelines, splitters)
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
