#!/usr/bin/python3.8

from collections import defaultdict
from functools import reduce
import sys

with open('input01.txt', 'rt') as f:
    num = [int(l.strip()) for l in f.readlines()]


def part1():
    m = set()
    for n in num:
        if (2020 - n) in m:
            pair = [2020-n, n]
            break
        m.add(n)
    else:
        print("No pair found")
        sys.exit(1)

    print(f"{pair} -> {pair[0] * pair[1]}")


def part2():
    for i, a in enumerate(num):
        for j, b in enumerate(num[i+1:]):
            for c in num[j+1:]:
                if a + b + c == 2020:
                    print(f"[{a}, {b}, {c}] -> {a*b*c}")
                    return
    print("No triplet found")


# part1()
# part2()


def components(num, n, target):
    """Assuming that there is only 1 way of adding `n` members
    of `num` to get `target`"""
    d = defaultdict(list)
    for x in num:
        if x > target:
            continue

        p = defaultdict(list)
        for val, comps in d.items():
            tval = val + x
            if tval > target:
                continue
            for comp in comps:
                tcomp = comp + [x]
                if len(tcomp) == n:
                    if tval == target:
                        print(f"{tcomp} -> {reduce(lambda x, y: x * y, tcomp)}")
                else:
                    p[tval] += [tcomp]

        d[x] += [[x]]
        for k, v in p.items():
            d[k] += v


components(num, 2, 2020)
components(num, 3, 2020)
