#!/usr/bin/python3.8

from pyaoc import Env
import re

e = Env(4)
e.T("""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""", 2, 4)

def make_pairs(lines):
    nums = re.compile(r'\d+')
    pairs = []
    for ln in lines:
        n = [int(x) for x in nums.findall(ln)]
        assert len(n) == 4, f'wrong number of numbers in "{ln}"'
        pairs.append(((n[0], n[1]), (n[2], n[3])))
    return pairs

def full_overlap(first, second):
    if first[0] >= second[0] and first[1] <= second[1]:
        return True
    if second[0] >= first[0] and second[1] <= first[1]:
        return True
    return False


def any_overlap(first, second):
    if first[1] < second[0] or second[1] < first[0]:
        return False
    return True


def part1(input):
    pairs = make_pairs(input.get_valid_lines())
    return sum([1 for first, second in pairs if full_overlap(first, second)])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pairs = make_pairs(input.get_valid_lines())
    return sum([1 for first, second in pairs if any_overlap(first, second)])


e.run_tests(2, part2)
e.run_main(2, part2)
