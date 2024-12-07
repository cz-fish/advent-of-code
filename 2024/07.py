#!/usr/bin/python3.12

from pyaoc import Env

e = Env(7)
e.T("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""", 3749, 11387)


def parse_input(input):
    records = []
    for ln in input.get_valid_lines():
        test_s, rest = ln.split(": ")
        test = int(test_s)
        vals = [int(x) for x in rest.split()]
        records.append((test, vals))
    return records


def calculate(test, vals, pos, running):
    if pos == len(vals):
        return running == test
    if running > test:
        return False
    return calculate(test, vals, pos + 1, running + vals[pos]) or calculate(test, vals, pos + 1, running * vals[pos])


def formula_match(test, vals):
    return calculate(test, vals, 1, vals[0])


def part1(input):
    records = parse_input(input)
    return sum([test for test, vals in records if formula_match(test, vals)])


e.run_tests(1, part1)
e.run_main(1, part1)

def concatenate(a, b):
    return int(str(a) + str(b))


def calculate2(test, vals, pos, running):
    if pos == len(vals):
        return running == test
    if running > test:
        return False
    return calculate2(test, vals, pos + 1, running + vals[pos]) or \
           calculate2(test, vals, pos + 1, running * vals[pos]) or \
           calculate2(test, vals, pos + 1, concatenate(running , vals[pos]))


def formula_match2(test, vals):
    return calculate2(test, vals, 1, vals[0])


def part2(input):
    records = parse_input(input)
    return sum([test for test, vals in records if formula_match2(test, vals)])


e.run_tests(2, part2)
e.run_main(2, part2)
