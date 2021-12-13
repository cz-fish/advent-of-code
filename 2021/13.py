#!/usr/bin/python3.8

from aoc import Env
import re

e = Env(13)
#e = Env(13, different_input='input13_alter.txt')
e.T("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""", 17, True)


def get_dots(lines):
    dots = set()
    for ln in lines:
        x, y = [int(v) for v in ln.split(',')]
        dots.add((x, y))
    return dots


def fold(dots, instr):
    r = re.compile(r'along ([xy])=(\d+)')
    m = r.search(instr)
    assert m is not None
    axis = m.group(1)
    coord = int(m.group(2))
    new_dots = set()
    for x, y in dots:
        if axis == 'x' and x < coord or axis == 'y' and y < coord:
            new_dots.add((x, y))
        elif axis == 'x':
            new_dots.add((2 * coord - x, y))
        else:
            new_dots.add((x, 2 * coord - y))
    return new_dots


def part1(input):
    gr = input.get_groups()
    dots = get_dots(gr[0])
    dots = fold(dots, gr[1][0])
    return len(dots)


e.run_tests(1, part1)
e.run_main(1, part1)


def print_dots(dots):
    minx = None
    maxx = None
    miny = None
    maxy = None
    for x,y in dots:
        if minx is None or x < minx:
            minx = x
        if maxx is None or x > maxx:
            maxx = x
        if miny is None or y < miny:
            miny = y
        if maxy is None or y > maxy:
            maxy = y
    w = maxx - minx + 1
    h = maxy - miny + 1
    out = [[' ' for _ in range(w)] for _ in range(h)]
    for x, y in dots:
        out[y - miny][x - minx] = '#'
    for row in out:
        print(''.join(row))


def part2(input):
    gr = input.get_groups()
    dots = get_dots(gr[0])
    for instr in gr[1]:
        dots = fold(dots, instr)
    print_dots(dots)
    return True


e.run_tests(2, part2)
e.run_main(2, part2)
