#!/usr/bin/python3.12

from pyaoc import Env

e = Env(3)
e.T("""987654321111111
811111111111119
234234234234278
818181911112111""", 357, 3121910778619)


def joltage2(line):
    assert len(line) >= 2
    first = sorted(line[:-1])[-1]
    first_index = line.index(first)
    second = sorted(line[first_index+1:])[-1]
    return int(first + second)


def joltage(line, remaining):
    assert len(line) >= remaining, f"{line} {remaining}"
    remaining -= 1
    first = sorted(line[:len(line) - remaining])[-1]
    if remaining == 0:
        return first
    else:
        first_index = line.index(first)
        rest = line[first_index+1:]
        return first + joltage(rest, remaining)


def part1(input):
    total = 0
    for ln in input.get_valid_lines():
        total += int(joltage(ln, 2))
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    total = 0
    for ln in input.get_valid_lines():
        total += int(joltage(ln, 12))
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
