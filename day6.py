#!/usr/bin/env python3

pts = []
minx = None
miny = None
maxx= None
maxy = None

with open('day6.txt', 'rt') as f:
    for l in f.readlines():
        l = l.strip()
        x, y = tuple([int(x) for x in l.split(', ')])
        if minx is None or x < minx: minx = x
        if miny is None or y < miny: miny = y
        if maxx is None or x > maxx: maxx = x
        if maxy is None or y > maxy: maxy = y
        pts += [(x,y)]

print (minx, miny, maxx, maxy)

w = maxx-minx+1
h = maxy-miny+1

clos = []
for i in range(maxy+1):
    clos += [[]]
    for j in range(maxx+1):
        clos[-1] += [-1]

counters = {}
for i in range(len(pts)):
    counters[i] = 0

for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        mind = None
        closest = None
        tie = False
        for i, p in enumerate(pts):
            dist = abs(p[0]-x) + abs(p[1]-y)
            if mind is None or dist < mind:
                mind = dist
                closest = i
                tie = False
            elif mind == dist:
                tie = True
        if not tie:
            clos[y][x] = closest
            counters[closest] += 1

inf = set()
for x in range(minx, maxx+1):
    inf.add(clos[miny][x])
    inf.add(clos[maxy][x])
for y in range(miny, maxy+1):
    inf.add(clos[y][minx])
    inf.add(clos[y][maxx])

biggest = None
count = None
for k,v in counters.items():
    if k in inf: continue
    if count is None or v > count:
        count = v
        biggest = k

print (count)

