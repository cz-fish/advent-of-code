#!/usr/bin/python3.8

from aoc import Env
from collections import Counter

e = Env(2)
e.T("""abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""", 12, None)
e.T("""abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""", None, 'fgij')


def part1(input):
    ids = input.get_valid_lines()
    twos = 0
    threes = 0
    for id in ids:
        counts = Counter(id)
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    return twos * threes


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    ids = input.get_valid_lines()
    length = len(ids[0])
    for first in ids:
        for second in ids:
            diff = [first[i] for i in range(length) if first[i] == second[i]]
            if len(diff) == length - 1:
                return ''.join(diff)
    assert False, "no solution found"


e.run_tests(2, part2)
e.run_main(2, part2)
