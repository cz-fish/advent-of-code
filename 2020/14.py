#!/usr/bin/python3.8

from aoc import Env
from collections import deque

import re

e = Env(14)
e.T("""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""", 165, None)
e.T("""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""", None, 208)


def parse_mask(maskstr):
    o = {}
    for i, c in enumerate(maskstr[::-1]):
        if c in '01':
            o[i] = int(c)
    return o


def apply_mask(mask, val):
    for p, v in mask.items():
        if v == 1:
            val = val | (2 ** p)
        elif v == 0:
            val = val & ~(2 ** p)
    return val


def part1(input):
    mask = {}
    mem = {}
    for ln in input.get_valid_lines():
        if ln.startswith('mask = '):
            mask = parse_mask(ln[7:])
        else:
            m = re.match(r'^mem\[(\d+)\] = (\d+)', ln)
            assert m is not None
            addr = int(m.group(1))
            val = int(m.group(2))
            mem[addr] = apply_mask(mask, val)
    return sum(mem.values())


e.run_tests(1, part1)
e.run_main(1, part1)


def write_with_mask(mem, addr, mask, val):
    exp = deque()
    exp.append((0, 0))
    while exp:
        i, a = exp.popleft()
        if i == 36:
            mem[a] = val
        else:
            if i in mask:
                if mask[i] == 1:
                    x = 1
                else:
                    x = (addr // (2**i)) & 1
                exp.append((i + 1, a + (2**i) * x))
            else:
                exp.append((i + 1, a))
                exp.append((i + 1, a + 2**i))


def part2(input):
    mask = {}
    mem = {}
    for ln in input.get_valid_lines():
        if ln.startswith('mask = '):
            mask = parse_mask(ln[7:])
        else:
            m = re.match(r'^mem\[(\d+)\] = (\d+)', ln)
            assert m is not None
            addr = int(m.group(1))
            val = int(m.group(2))
            write_with_mask(mem, addr, mask, val)
    return sum(mem.values())


e.run_tests(2, part2)
e.run_main(2, part2)
