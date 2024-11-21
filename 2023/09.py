#!/usr/bin/python3.8

from pyaoc import Env

e = Env(9)
e.T("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""", 114, 2)

def predict(nums, forward):
    assert len(nums) >= 2
    all0 = True
    diffs = []
    for i in range(len(nums)-1):
        diffs.append(nums[i+1]-nums[i])
        if diffs[-1] != 0:
            all0 = False
    if all0:
        return 0
    else:
        if forward:
            return predict(diffs, forward) + diffs[-1]
        else:
            return diffs[0] - predict(diffs, forward)

def part1(input):
    seq = [[int(x) for x in ln.split()] for ln in input.get_valid_lines()]
    nums = [s[-1] + predict(s, True) for s in seq]
    return sum(nums)

e.run_tests(1, part1)
e.run_main(1, part1)

def part2(input):
    seq = [[int(x) for x in ln.split()] for ln in input.get_valid_lines()]
    nums = [s[0] - predict(s, False) for s in seq]
    return sum(nums)

e.run_tests(2, part2)
e.run_main(2, part2)
