#!/usr/bin/python3.8

# Note: https://oeis.org/A181391

from aoc import Env

e = Env(15)
e.T("0,3,6", 436, 175594)


def van_eck(start, K):
    memory = dict([(c, i) for i, c in enumerate(start)])
    last_said = start[-1]
    memory = {}
    turn = 1
    next = start[0]

    while turn <= K:
        # elf says next
        # print(f"turn {turn}: {next}")
        last_said = next
        if turn < len(start):
            next = start[turn]
        else:
            # when was that said last time
            if last_said in memory:
                next = turn - memory[last_said]
            else:
                next = 0
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
