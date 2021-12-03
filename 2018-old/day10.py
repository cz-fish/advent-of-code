#!/usr/bin/env python3

import re

points = []
with open('day10.txt', 'rt') as f:
    for l in f.readlines():
        t = [int(i) for i in re.match(r'position=<([^,]+),([^>]+)> velocity=<([^,]+),([^>]+)', l).groups()]
        points += [t]

def minmax(points):
    minx = None
    miny = None
    maxx = None
    maxy = None
    for p in points:
        if minx == None or p[0] < minx:
            minx = p[0]
        if maxx == None or p[0] > maxx:
            maxx = p[0]
        if miny == None or p[1] < miny:
            miny = p[1]
        if maxy == None or p[1] > maxy:
            maxy = p[1]
    return (minx, miny, maxx, maxy)

def move(points, n = 1):
    for p in points:
        p[0] += n * p[2]
        p[1] += n * p[3]



move(points, 10630)
minx, miny, maxx, maxy = minmax(points)

if False:
    minw = None
    minh = None
    minwt = None
    minht = None

    for t in range(10000):
        minx, miny, maxx, maxy = minmax(points)
        w = maxx-minx
        h = maxy-miny
        if minw == None or w < minw:
            minw = w
            minwt = t
        if minh == None or h < minh:
            minh = h
            minht = t
        move(points)

    print (minh, minht, minw, minwt)

plot = []
for i in range(10):
    plot += [[]]
    for j in range(80):
        plot[i] += [' ']

for p in points:
    plot[p[1]-miny][p[0]-minx] = '#'

for i in range(10):
    print(''.join(plot[i]))