#!/usr/bin/python3.12

from pyaoc import Env
import re

e = Env(14, param=(101, 103))
e.T("""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""", 12, None, param=(11, 7))


def parse_input(input):
    robots = []
    num_re = re.compile(r'-?\d+')
    for ln in input.get_valid_lines():
        numbers = [int(x) for x in num_re.findall(ln)]
        assert len(numbers) == 4
        robots.append(tuple(numbers))
    return robots


def count_quadrants(robots, size, steps):
    quads = [0, 0, 0, 0]
    mid_x = size[0] // 2
    mid_y = size[1] // 2
    for x, y, dx, dy in robots:
        f_x = (x + steps * dx) % size[0]
        f_y = (y + steps * dy) % size[1]
        if f_x == mid_x or f_y == mid_y:
            # robot on the quadrant boundary
            continue
        index = 0
        if f_x > mid_x:
            index += 2
        if f_y > mid_y:
            index += 1
        quads[index] += 1
    return quads


def part1(input):
    robots = parse_input(input)
    size = e.get_param()
    quadrants = count_quadrants(robots, size, 100)
    safety = 1
    for q in quadrants:
        safety *= q
    return safety


e.run_tests(1, part1)
e.run_main(1, part1)


def print_robots(step, robots, size):
    grid = [['.' for _ in range(size[0])] for _ in range(size[1])]
    for x, y, dx, dy in robots:
        px = (x + dx * step) % size[0]
        py = (y + dy * step) % size[1]
        grid[py][px] = '#'
    lines = []
    print_this = False
    for row in grid:
        lines.append(''.join(row))
        if '###############################' in lines[-1]:
            print_this = True
    if print_this:
        print(f"={step}===========")
        for ln in lines:
            print(ln)
    return print_this


def part2(input):
    robots = parse_input(input)
    size = e.get_param()
    for i in range(10000):
        if print_robots(i, robots, size):
            return i
    return 0


# e.run_tests(2, part2)
e.run_main(2, part2)
