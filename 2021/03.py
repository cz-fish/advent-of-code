#!/usr/bin/python3.8

from aoc import Env

e = Env(3)
e.T("""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""", 198, 230)


def part1(input):
    lines = input.get_valid_lines()
    width = len(lines[0])
    counters = [0] * width
    for ln in lines:
        for i, c in enumerate(ln):
            if c == '1':
                counters[i] += 1
    gamma = ''
    epsilon = ''
    threshold = len(lines) // 2
    for p in range(width):
        if counters[p] > threshold:
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    print(f'gamma: {gamma}')
    print(f'epsilon: {epsilon}')
    g = int(gamma, 2)
    e = int(epsilon, 2)
    return g * e


e.run_tests(1, part1)
e.run_main(1, part1)


def filter(remaining, type, pos):
    if len(remaining) == 1:
        return remaining.pop()
    threshold = len(remaining) / 2
    count = 0
    splits = {'0': set(), '1': set()}
    for ln in remaining:
        if ln[pos] == '1':
            count += 1
        splits[ln[pos]].add(ln)
    remove = '0'
    if (type == 1 and count < threshold) or (type == 0 and count >= threshold):
        remove = '1'
    remaining = remaining - splits[remove]
    return filter(remaining, type, pos+1)


def part2(input):
    linesL = input.get_valid_lines()
    width = len(linesL[0])
    lines = set(linesL)
    oxygen = int(filter(lines, 1, 0), 2)
    lines = set(linesL)
    co2 = int(filter(lines, 0, 0), 2)
    print(f'oxygen {oxygen}')
    print(f'co2 {co2}')
    return oxygen * co2


e.run_tests(2, part2)
e.run_main(2, part2)
