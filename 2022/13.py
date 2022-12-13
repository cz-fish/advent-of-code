#!/usr/bin/python3.8

from aoc import Env
import functools
import json

e = Env(13)
e.T("""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""", 13, 140)


def get_pairs(input):
    groups = input.get_groups()
    pairs = []
    for gr in groups:
        assert len(gr) == 2
        pairs.append((
            json.loads(gr[0]),
            json.loads(gr[1])
        ))
    return pairs


def compare(left, right):
    if type(left) == int:
        if type(right) == int:
            # integer comparison
            if left < right:
                return -1
            elif right < left:
                return 1
            else:
                return 0
        else:
            # mixed, promote left to list
            return compare([left], right)
    else:
        if type(right) == int:
            # mixed, promote right to list
            return compare(left, [right])
        else:
            # list comparison
            for i in range(min(len(left), len(right))):
                c = compare(left[i], right[i])
                if c != 0:
                    return c
            if len(left) < len(right):
                return -1
            elif len(right) < len(left):
                return 1
            else:
                return 0


def in_order(pair):
    return True if compare(pair[0], pair[1]) <= 0 else False


def part1(input):
    pairs = get_pairs(input)
    return sum([i+1 for i, pair in enumerate(pairs) if in_order(pair)])


e.run_tests(1, part1)
e.run_main(1, part1)


def find_index(haystack, needle):
    for i, value in enumerate(haystack):
        if compare(value, needle) == 0:
            return i+1
    assert False, f'value {needle} not found'


def part2(input):
    values = [json.loads(s) for s in input.get_valid_lines()]
    values.append([[2]])
    values.append([[6]])
    values.sort(key=functools.cmp_to_key(compare))
    return find_index(values, [[2]]) * find_index(values, [[6]])


e.run_tests(2, part2)
e.run_main(2, part2)
