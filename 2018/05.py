#!/usr/bin/python3.8

from aoc import Env

e = Env(5)
e.T("dabAcCaCBAcCcaDA", 10, 4)


def reduce(line):
    crush = []
    for c in line:
        if crush and crush[-1].lower() == c.lower() and crush[-1] != c:
            crush.pop()
        else:
            crush.append(c)
    return len(crush)


def part1(input):
    line = input.get_lines()[0]
    return reduce(line)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    m = None
    orig_line = input.get_lines()[0]

    for c in 'abcdefghijklmnopqrstuvwxyz':
        C = c.upper()
        line = orig_line.replace(c, '').replace(C, '')
        size = reduce(line)
        if m is None or size < m:
            m = size
    return m


e.run_tests(2, part2)
e.run_main(2, part2)
