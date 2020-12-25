#!/usr/bin/python3.8

from aoc import Env

e = Env(1)
e.T("""+1
+1
+1""", 3, None)
e.T("""+1
+1
-2""", 0, None)
e.T("""-1
-2
-3""", -6, None)
e.T("""+1
-2
+3
+1""", None, 2)


def part1(input):
    ints = [int(x) for x in input.get_valid_lines()]
    return sum(ints)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    ints = [int(x) for x in input.get_valid_lines()]
    c = 0
    s = set()
    while True:
        for x in ints:
            c += x
            if c in s:
                return c
            s.add(c)


e.run_tests(2, part2)
e.run_main(2, part2)
