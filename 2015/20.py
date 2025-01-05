#!/usr/bin/python3.12

from pyaoc import Env
import math

e = Env(20)

def sigma(num):
    sq = int(math.floor(math.sqrt(num)))
    tot = 0
    for i in range(1, sq + 1):
        d = num // i
        if d * i == num:
            tot += i
            if d != i:
                tot += d
    return tot


def part1(input):
    v = input.get_ints()
    assert len(v) == 1
    target = int(v[0])
    for i in range(1, target):
        if sigma(i) * 10 >= target:
            return i
    assert False, "solution not found"


e.run_tests(1, part1)
e.run_main(1, part1)


def sigma50(num):
    sq = int(math.floor(math.sqrt(num)))
    tot = 0
    for i in range(1, sq + 1):
        d = num // i
        if d * i == num:
            if d <= 50:
                tot += i
            if d != i and i <= 50:
                tot += d
    return tot


def part2(input):
    # 50 houses each, 11x elves number
    v = input.get_ints()
    assert len(v) == 1
    target = int(v[0])
    # assumption - part2 will be higher than part1, so we
    # can start iterating from part1 solution (rough)
    for i in range(780000, target):
        s = sigma50(i) * 11
        if s >= target:
            return i
    assert False, "solution not found"


e.run_tests(2, part2)
e.run_main(2, part2)
