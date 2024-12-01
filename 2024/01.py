#!/usr/bin/python3.12

from pyaoc import Env
from collections import Counter

e = Env(1)
e.T("""3   4
4   3
2   5
1   3
3   9
3   3""", 11, 31)


def make_number_lists(input):
    lines = input.get_valid_lines()
    numbers = [[int(v) for v in ln.split()] for ln in lines]
    list0 = [x[0] for x in numbers]
    list1 = [x[1] for x in numbers]
    return list0, list1


def part1(input):
    list0, list1 = make_number_lists(input)
    list0.sort()
    list1.sort()
    return sum([abs(d[0] - d[1]) for d in zip(list0, list1)])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    list0, list1 = make_number_lists(input)
    c = Counter(list1)
    return sum([v * c[v] for v in list0 if v in c])


e.run_tests(2, part2)
e.run_main(2, part2)
