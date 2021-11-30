#!/usr/bin/python3.8

from aoc import Env

e = Env(8)
e.T("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2", 138, 66)

def build_tree(nums, start):
    n_child = nums[start]
    n_meta = nums[start+1]
    start += 2
    nodes = []
    for j in range(n_child):
        start, node = build_tree(nums, start)
        nodes.append(node)
    meta = nums[start : start + n_meta]
    return start + n_meta, {
        'n': nodes,
        'm': meta
    }


def sum_meta(tree):
    s = 0
    for n in tree['n']:
        s += sum_meta(n)
    s += sum(tree['m'])
    return s


def part1(input):
    nums = input.get_all_ints()
    x, tree = build_tree(nums, 0)
    assert(x == len(nums))
    return sum_meta(tree)


e.run_tests(1, part1)
e.run_main(1, part1)


def sum_children(tree):
    n = tree['n']
    if not n:
        return sum(tree['m'])
    s = 0
    for c in tree['m']:
        if c == 0 or c > len(n):
            continue
        s += sum_children(n[c - 1])
    return s


def part2(input):
    nums = input.get_all_ints()
    x, tree = build_tree(nums, 0)
    assert(x == len(nums))
    return sum_children(tree)


e.run_tests(2, part2)
e.run_main(2, part2)
