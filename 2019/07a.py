#!/usr/bin/env python3
import sys
import intcode
from itertools import permutations

with open('input07.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

amps = list(range(5))
best = 0

for p in permutations(amps):
    prev = 0

    for a in p:
        inarray = [a, prev]
        inpos = 0

        def input_fn():
            global inpos
            v = inarray[inpos]
            inpos += 1
            return v

        mach = intcode.IntCode(program)
        mach.run(input_fn)
        prev = mach.output[-1]

    print(p, prev)

    if prev > best:
        best = prev

print(best)