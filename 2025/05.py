#!/usr/bin/python3.12

from pyaoc import Env

e = Env(5)
e.T("""3-5
10-14
16-20
12-18

1
5
8
11
17
32""", 3, 14)


def parse_intervals(lines):
    intervals = []
    for ln in lines:
        p = ln.split('-')
        assert len(p) == 2
        intervals.append((int(p[0]), int(p[1])))
    return intervals


def part1(input):
    g = input.get_groups()
    assert len(g) == 2
    intervals = parse_intervals(g[0])
    vals = [int(x) for x in g[1]]
    fresh = 0
    for v in vals:
        for i in intervals:
            if v >= i[0] and v <= i[1]:
                fresh += 1
                break
    return fresh


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = input.get_groups()
    assert len(g) == 2
    intervals = parse_intervals(g[0])
    points = []
    for i in intervals:
        points.append((i[0], 1))
        points.append((i[1]+1, -1))
    points.sort()
    inout = 0
    start = None
    total = 0
    for x, d in points:
        if inout == 0:
            assert d == 1
            assert start is None
            start = x
        inout += d
        if d == -1:
            if inout == 0:
                assert start is not None
                total += x - start
                start = None
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
