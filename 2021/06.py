#!/usr/bin/python3.8

from pyaoc import Env
from collections import Counter

e = Env(6)
e.T('3,4,3,1,2', 5934, 26984457539)


def count_lanternfish_dumb(fish, after_days):
    for day in range(after_days):
        new = []
        for i, f in enumerate(fish):
            if f == 0:
                new += [8]
                fish[i] = 6
            else:
                fish[i] -= 1
        fish += new
    return len(fish)


def count_lanternfish_smarter(fish, after_days):
    counts = Counter(fish)
    born = {}
    nfish = len(fish)
    for d in range(after_days):
        num_new = 0
        # This day, the d%7-th generation will multiply
        # (if there are any fish in this generation)
        per = d % 7
        if per in counts:
            num_new += counts[per]
        # Those that were born 9 days ago will also multiply
        # for the first time
        prev = d - 9
        if prev in born:
            num_new += born[prev]
            # Going forward, the 9 days old fish will now also
            # belong to the d%7 generation
            if per not in counts:
                counts[per] = 0
            counts[per] += born[prev]
        # Add all the fish newly born today to the total
        nfish += num_new
        born[d] = num_new
    return nfish


def part1(input):
    fish = input.get_all_ints()
    return count_lanternfish_smarter(fish, 80)
    # return count_lanternfish_dumb(fish, 80)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    fish = input.get_all_ints()
    return count_lanternfish_smarter(fish, 256)


e.run_tests(2, part2)
e.run_main(2, part2)
