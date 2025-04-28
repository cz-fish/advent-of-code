#!/usr/bin/python3.12

from pyaoc import Env
from collections import Counter

e = Env(11)
e.T("ne,ne,ne", 3, None)
e.T("ne,ne,sw,sw", 0, None)
e.T("ne,ne,s,s", 2, None)
e.T("se,sw,se,sw,sw", 3, None)

e.T("ne,se", 2, None)
e.T("nw,ne,se", 1, None)
e.T("ne,ne,se,n", 3, None)
e.T("nw,nw,n", 3, None)


def distance(hops):
    d = {
        'n': (-2, 0),
        'nw': (-1, -1),
        'ne': (-1, 1),
        's': (2, 0),
        'sw': (1, -1),
        'se': (1, 1),
    }
    row = abs(sum([d[h][0] for h in hops]))
    col = abs(sum([d[h][1] for h in hops]))
    steps = col
    extra = (row - steps + 1) // 2
    if extra > 0:
        steps += extra
    return steps


def part1(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    hops = lines[0].split(',')
    return distance(hops)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
