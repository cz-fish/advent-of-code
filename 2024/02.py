#!/usr/bin/python3.12

from pyaoc import Env

e = Env(2)
e.T("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 2, 4)


def part1(input):
    safe = 0
    for ln in input.get_valid_lines():
        nums = [int(x) for x in ln.split()]
        diffs = [nums[i] - nums[i+1] for i in range(len(nums)-1)]
        all_inc = all([x > 0 for x in diffs])
        all_dec = all([x < 0 for x in diffs])
        small = all([abs(x) <= 3 for x in diffs])
        if (all_inc or all_dec) and small:
            safe += 1
    return safe


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
