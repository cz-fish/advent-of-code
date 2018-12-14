#!/usr/bin/env python3

import re

fabric = {}
counter = 0

lines = []
with open('day3.txt', 'rt') as f:
    for l in f.readlines():
        m = re.search(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', l)
        if not m:
            print('skipped {}'.format(l))
            continue

        lines += [tuple([int(i) for i in m.groups()])]

for  claim, left, top, width, height in lines:
    for i in range(left, left+width):
        for j in range(top, top+height):
            k = str(i) + '.' + str(j)
            if k in fabric:
                if fabric[k] == 1:
                    counter += 1
                fabric[k] += 1
            else:
                fabric[k] = 1

print(counter)

for  claim, left, top, width, height in lines:
    good = True
    for i in range(left, left+width):
        for j in range(top, top+height):
            k = str(i) + '.' + str(j)
            if fabric[k] > 1:
                good = False
                break
        if not good: break
    if good:
        print(claim)
        break
