#!/usr/bin/python3.8

from aoc import Env

e = Env(2)
e.T("""forward 5
down 5
forward 8
up 3
down 8
forward 2""", 150, 900)


def directions(lines):
    dirs = []
    for ln in lines:
        d, a = ln.strip().split(' ')
        dirs += [(d, int(a))]
    return dirs


def part1(input):
    dirs = directions(input.get_valid_lines())
    x = 0
    y = 0
    for d, a in dirs:
        if d == 'down':
            y += a
        elif d == 'up':
            y -= a
        elif d == 'forward':
            x += a
        else:
            assert False
    return x * y


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    dirs = directions(input.get_valid_lines())
    x = 0
    y = 0
    aim = 0
    for d, a in dirs:
        if d == 'down':
            aim += a
        elif d == 'up':
            aim -= a
        elif d == 'forward':
            x += a
            y += a * aim
        else:
            assert False
    return x * y
    pass


e.run_tests(2, part2)
e.run_main(2, part2)
