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

def summarize(area):
    return ''.join([''.join(r) for r in area])

cyc = {}
t = 0
v = summarize(area)
cyc[v] = t
mm = {t: v}
while True:
    area = step(area)
    t += 1
    v = summarize(area)
    if v in cyc:
        first = cyc[v]
        cycle = t - first
        print(t, first, cycle)
        break
    cyc[v] = t
    mm[t] = v
    if t % 1000 == 0:
        print('.', end='')
        sys.stdout.flush()

s = (1000000000 - first) % cycle
print('variant',s)
state = mm[first + s]
wood = len([c for c in state if c == '|'])
lumber = len([c for c in state if c == '#'])

print (wood, lumber, wood * lumber)