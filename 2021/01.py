#!/usr/bin/python3.8

from aoc import Env

e = Env(1)
e.T("""199
200
208
210
200
207
240
269
260
263""", 7, 5)


def part1(input):
    depths = input.get_all_ints()
    incs = sum([1 for i in range(1, len(depths)) if depths[i] > depths[i-1]])
    return incs


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    depths = input.get_all_ints()
    threes = [depths[i] + depths[i+1] + depths[i+2] for i in range(len(depths)-2)]
    incs = sum([1 for i in range(1, len(threes)) if threes[i] > threes[i-1]])
    return incs


e.run_tests(2, part2)
e.run_main(2, part2)
