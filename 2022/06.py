#!/usr/bin/python3.8

from aoc import Env

e = Env(6)
e.T("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19)
e.T("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23)
e.T("nppdvjthqldpwncqszvftbrmjlhg", 6, 23)
e.T("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29)
e.T("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26)


def find_start_packet(line, unique_cnt):
    repeat = -1
    seen = {}
    for i, c in enumerate(line):
        if c in seen:
            repeat = max(repeat, seen[c])
        seen[c] = i
        if i - repeat >= unique_cnt:
            return i + 1
    assert False, "no start of packet found"


def part1(input):
    return find_start_packet(input.get_valid_lines()[0], 4)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return find_start_packet(input.get_valid_lines()[0], 14)


e.run_tests(2, part2)
e.run_main(2, part2)
