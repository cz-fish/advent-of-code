#!/usr/bin/python3.8

from aoc import Env
import re
from collections import defaultdict

e = Env(5)
e.T("""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""", 5, 12)


def parse_coords(input):
    ints = input.get_all_ints()
    assert len(ints)%4 == 0
    coords = []
    for i in range(0, len(ints), 4):
        coords += [((ints[i], ints[i+1]), (ints[i+2], ints[i+3]))]
    return coords


def paint_line(A, B, counters):
    d = (B[0] - A[0], B[1] - A[1])
    if d[0] == 0:
        steps = abs(d[1])
    elif d[1] == 0:
        steps = abs(d[0])
    else:
        assert abs(d[0]) == abs(d[1])
        steps = abs(d[0])
    d = (d[0] // steps, d[1] // steps)
    assert d[0] != 0 or d[1] != 0
    while A != B:
        counters[A] += 1
        A = (A[0] + d[0], A[1] + d[1])
    counters[B] += 1


def count_more_than_1(counters):
    return len([1 for x in counters.values() if x > 1])


def part1(input):
    coords = parse_coords(input)
    counters = defaultdict(int)
    for A, B in coords:
        if A[0] != B[0] and A[1] != B[1]:
            continue
        paint_line(A, B, counters)
    return count_more_than_1(counters)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    coords = parse_coords(input)
    counters = defaultdict(int)
    for A, B in coords:
        paint_line(A, B, counters)
    return count_more_than_1(counters)


e.run_tests(2, part2)
e.run_main(2, part2)
