#!/usr/bin/python3.8

from pyaoc import Input
import sys
from collections import defaultdict

inp = Input('input09.txt', ["""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""])

preamb = 25

# test case
# inp.use_test(0)
# preamb = 5

nums = inp.get_ints()

target = None
run = set(nums[:preamb])
for i in range(preamb, len(nums)):
    num = nums[i]
    for j in run:
        remainder = num - j
        if remainder == j:
            continue
        if remainder in run:
            break
    else:
        target = num
        print(f"Part 1: first wrong: {num}")
        break
    run.remove(nums[i-preamb])
    run.add(num)
else:
    print("Part 1: no wrong num found")
    sys.exit(1)

# Part 2 - find seq that adds up to target
sums = defaultdict(int)
for i in range(len(nums)):
    num = nums[i]
    nsums = defaultdict(int)
    for k, v in sums.items():
        w = v + num
        if w == target:
            rng = nums[i-k:i+1]
            m, M = min(rng), max(rng)
            print(rng, m, M)
            print(f"Part 2: weakness: {m + M}")
            sys.exit(0)
        nsums[k+1] = w
    nsums[1] = num
    sums = nsums
else:
    print("Part 2: solution not found")

