#!/usr/bin/python3.8

from aoc import Env

e = Env(1)
e.T("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", 142, None)
e.T("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", None, 281)


def clean_numbers(lines):
    numbers = []
    for ln in lines:
        first = None
        last = None
        for c in ln:
            if c >= '0' and c <= '9':
                if first is None:
                    first = int(c)
                last = int(c)
        assert first is not None and last is not None, f"Line {ln}"
        numbers.append(first * 10 + last)
    return numbers


def part1(input):
    lines = input.get_valid_lines()
    numbers = clean_numbers(lines)
    return sum(numbers)


e.run_tests(1, part1)
e.run_main(1, part1)


def clean_spelled_numbers(lines):
    numbers = []
    words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for ln in lines:
        matches = []

        # Find first and last occurrence (if different) of given key
        def find_first_and_last(key, val):
            nonlocal matches
            p = ln.find(key)
            if p != -1:
                matches.append((p, val))
                q = ln.rfind(key)
                if q != p:
                    matches.append((q, val))

        # Spelled out numbers
        for k, v in words.items():
            find_first_and_last(k, v)
        # Digit characters
        for v in range(10):
            find_first_and_last(str(v), v)

        first = min(matches)
        last = max(matches)
        val = first[1] * 10 + last[1]
        numbers.append(val)
    return numbers


def part2(input):
    lines = input.get_valid_lines()
    numbers = clean_spelled_numbers(lines)
    return sum(numbers)


e.run_tests(2, part2)
e.run_main(2, part2)
