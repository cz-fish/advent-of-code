#!/usr/bin/python3.12

from pyaoc import Env

e = Env(2)
e.T("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""", 1227775554, 4174379265)


def is_invalid(id_str, periods):
    if len(id_str) % periods == 0:
        group = id_str[:len(id_str)//periods]
        return id_str == group * periods
    return False


def scan_interval(start, end, halves_only):
    total = 0
    for i in range(start, end+1):
        s = str(i)
        if halves_only:
            if is_invalid(s, 2):
                total += i
        else:
            for p in range(2, len(s) + 1):
                if is_invalid(s, p):
                    #print(s, p)
                    total += i
                    break
    return total


def sum_invalid_ids(input, halves_only):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    intervals = lines[0].split(',')
    total = 0
    for interval in intervals:
        ends = interval.split('-')
        assert len(ends) == 2
        total += scan_interval(int(ends[0]), int(ends[1]), halves_only)
    return total


def part1(input):
    return sum_invalid_ids(input, True)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return sum_invalid_ids(input, False)


e.run_tests(2, part2)
e.run_main(2, part2)
