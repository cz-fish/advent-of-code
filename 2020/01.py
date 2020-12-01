#!/usr/bin/python3.8

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
            for k, c in enumerate(num[j+1:]):
                if a + b + c == 2020:
                    print(f"[{a}, {b}, {c}] -> {a*b*c}")
                    return
    print("No triplet found")


part1()
part2()
