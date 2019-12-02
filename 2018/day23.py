#!/usr/bin/env python3

import re

bots = []
strongest = None
strength = 0

with open('inputs/day23.txt', 'rt') as f:
    for i, l in enumerate(f.readlines()):
        m = re.match(r'^pos=<([^,]+),([^,]+),([^>]+)>, r=(\d+)', l)
        x, y, z, r = tuple([int(x) for x in m.groups()])
        bots += [(x,y,z,r)]
        if r > strength:
            strongest = i
            strength = r

snb = bots[strongest]
ln = len(bots)

inrange = 0

for i, b in enumerate(bots):
    dist = abs(b[0] - snb[0]) + abs(b[1] - snb[1]) + abs(b[2] - snb[2])
    if dist <= snb[3]:
        inrange += 1


print(inrange)

pairs = [False] * (ln * ln)

for i in range(ln):
    b = bots[i]
    for j in range(i+1, ln):
        c = bots[j]
        dist = abs(b[0] - c[0]) + abs(b[1] - c[1]) + abs(b[2] - c[2])
        if dist < b[3] + c[3]:
            pairs[i * ln + j] = True

biggest = None
#most_distant = None
sets = []

for seed in range(ln):
    print("seed", seed)
    in_set = [0] * ln
    for x in range(ln):
        if x == seed: continue
        if (x < seed and not pairs[x*ln + seed]) or (x > seed and not pairs[seed * ln + x]): continue
        for y in range(x):
            if y == seed or not in_set[y]: continue
            if not pairs[y * ln + x]:
                break
        else:
            in_set[x] = 1
    s = sum(in_set)
    if biggest is None or s > biggest:
        biggest = s
        sets = [in_set]
    elif s == biggest:
        for x in sets:
            if x == in_set:
                break
        else:
            sets += [in_set]

print(biggest, len(sets))
#for s in sets:
#    print([l for l in range(ln) if s[l]])

print([l for l in range(ln) if sets[0][l]])
        
