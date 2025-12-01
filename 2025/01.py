#!/usr/bin/python3.12

from pyaoc import Env

e = Env(1)
e.T("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 3, 6)


def parse_input(input):
    instr = []
    for ln in input.get_valid_lines():
        d = ln[0]
        a = int(ln[1:])
        assert d in "LR"
        assert a > 0
        instr.append((d, a))
    return instr


def part1(input):
    instr = parse_input(input)
    val = 50
    count = 0
    for d, a in instr:
        if d == 'L': a = -a
        val = (val + a) % 100
        if val == 0:
            count += 1
    return count


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    instr = parse_input(input)
    val = 50
    count = 0
    for d, a in instr:
        o = a
        if a >= 100:
            count += a // 100
            a = a % 100
        if d == 'L': a = -a
        y = val + a
        if (y <= 0 and val > 0) or y >= 100:
            #print(f"{d}{o}' {val} -> {y}")
            count += 1
        val = y % 100
    return count


e.run_tests(2, part2)
e.run_main(2, part2)
