#!/usr/bin/python3.8

from aoc import Env

e = Env(2)
e.T("""A Y
B X
C Z""", 15, 12)

LOSE = 0
WIN = 6
DRAW = 3


def make_scoring():
    scoring = {}
    for first in 'ABC':
        for second in 'XYZ':
            a = ord(first) - ord('A')
            b = ord(second) - ord('X')
            win = DRAW if a == b else (LOSE if (b + 1) % 3 == a else WIN)
            scoring[(first, second)] = (b + 1) + win
    return scoring


def make_guide():
    guide = {}
    for first in 'ABC':
        for second in 'XYZ':
            a = ord(first) - ord('A')
            if second == 'X':
                score = LOSE + (a - 1) % 3 + 1
            elif second == 'Y':
                score = DRAW + a + 1
            else:
                score = WIN + (a + 1) % 3 + 1
            guide[(first, second)] = score
    return guide


def part1(input):
    scoring = make_scoring()
    return sum([scoring[(a, b)] for a, b in map(lambda ln: ln.split(' '), input.get_valid_lines())])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    guide = make_guide()
    return sum([guide[(a, b)] for a, b in map(lambda ln: ln.split(' '), input.get_valid_lines())])


e.run_tests(2, part2)
e.run_main(2, part2)
