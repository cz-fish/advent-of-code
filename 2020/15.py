#!/usr/bin/python3.8

# Note: https://oeis.org/A181391

from pyaoc import Env
import numpy

e = Env(15)
e.T("0,3,6", 436, 175594)


def van_eck(start, K):
    memory = numpy.zeros(K, dtype=int)

    for i, x in enumerate(start):
        memory[x] = i + 1

    last_said = 0
    # Assuming all numbers in start are unique
    next = 0
    turn = len(start) + 1

    while turn <= K:
        # elf says next
        last_said = next
        # when was that said last time
        next = memory[last_said]
        if next != 0:
            next = turn - next
        memory[last_said] = turn
        turn += 1
    return last_said


def get_start_vector(input):
    line = input.get_valid_lines()[0]
    return [int(x) for x in line.split(',')]


def part1(input):
    return van_eck(get_start_vector(input), 2020)


def part2(input):
    return van_eck(get_start_vector(input), 30000000)


e.run_tests(1, part1)
e.run_main(1, part1)
e.run_tests(2, part2)
e.run_main(2, part2)
