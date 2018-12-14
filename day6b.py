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

counter = 0

for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        s = 0
        for i, p in enumerate(pts):
            s += abs(p[0]-x) + abs(p[1]-y)
        if s < 10000:
            counter += 1

print(counter)


