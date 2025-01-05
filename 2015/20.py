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


def part2(input):
    # 50 houses each, 11x elves number
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
