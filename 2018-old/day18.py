#!/usr/bin/env python3
import sys

area = []
with open('inputs/day18.txt', 'rt') as f:
    for ll in f.readlines():
        area += [[c for c in ll.strip()]]

h = len(area)
w = len(area[0])

def count(area, x, y):
    ground = 0
    trees = 0
    lumber = 0
    for i in range(max(0,x-1), min(w,x+2)):
        for j in range(max(0,y-1), min(h,y+2)):
            if i == x and j == y: continue
            c = area[j][i]
            if c == '.': ground += 1
            elif c == '|': trees += 1
            elif c == '#': lumber += 1
    return ground, trees, lumber

def step(area):
    narea = []
    for y, row in enumerate(area):
        narea += [[]]
        for x, c in enumerate(row):
            ground, trees, lumber = count(area, x, y)
            if c == '.' and trees >= 3:
                x = '|'
            elif c == '|' and lumber >= 3:
                x = '#'
            elif c == '#' and (trees < 1 or lumber < 1):
                x = '.'
            else:
                x = c
            narea[-1] += [x]
    return narea

for t in range(10):
    area = step(area)

wood = 0
lumber = 0
for r in area:
    for c in r:
        if c == '|': wood += 1
        elif c == '#': lumber += 1
print (wood, lumber, wood * lumber)