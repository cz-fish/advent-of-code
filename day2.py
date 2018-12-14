#!/usr/bin/env python3

import sys

f = open('day2.txt', 'rt')
l = [x.strip() for x in list(f.readlines())]

def count(x):
    p = {}
    for c in x:
        if c not in p:
            p[c] = 0
        p[c] += 1
    two = False
    three = False
    for k,v in p.items():
        if v == 2: two=True
        if v == 3: three = True
    return ([0,1][two], [0,1][three])

twos = 0
threes = 0
for i in l:
    t2,t3 = count(i)
    twos += t2
    threes += t3

print(twos * threes)

def diffs(a, b):
    same = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            same += a[i]
    if len(same) == len(a) - 1:
        print(same)
        sys.exit(0)

for i in l:
    for j in l:
        diffs(i, j)
        