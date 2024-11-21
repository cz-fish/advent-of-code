#!/usr/bin/python3.8

from pyaoc import Env

e = Env(1)
e.T("""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""", 24000, 45000)


def part1(input):
    elves = [[int(ln) for ln in elf] for elf in input.get_groups()]
    return max([sum(elf) for elf in elves])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    elves = [sum([int(ln) for ln in elf]) for elf in input.get_groups()]
    elves.sort()
    assert len(elves) >= 3, "not enough elves"
    return sum(elves[-3:])


e.run_tests(2, part2)
e.run_main(2, part2)
