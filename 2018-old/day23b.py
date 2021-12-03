#!/usr/bin/env python3

import re
import heapq
import sys

bots = []
strongest = None
strength = 0

mins = [None, None, None]
maxes = [None, None, None]

with open('inputs/day23.txt', 'rt') as f:
    for i, l in enumerate(f.readlines()):
        m = re.match(r'^pos=<([^,]+),([^,]+),([^>]+)>, r=(\d+)', l)
        x, y, z, r = tuple([int(x) for x in m.groups()])
        bots += [(x,y,z,r)]
        if r > strength:
            strongest = i
            strength = r
        if mins[0] is None:
            mins[0] = x - r
            mins[1] = y - r
            mins[2] = z - r
            maxes[0] = x + r
            maxes[1] = y + r
            maxes[2] = z + r
        else:
            if x - r < mins[0]: mins[0] = x - r
            if y - r < mins[1]: mins[1] = y - r
            if z - r < mins[2]: mins[2] = z - r
            if x + r > maxes[0]: maxes[0] = x + r
            if y + r > maxes[1]: maxes[1] = y + r
            if z + r > maxes[2]: maxes[2] = z + r

snb = bots[strongest]
ln = len(bots)

inrange = 0

def dist(a, b):
    return sum([abs(a[i]-b[i]) for i in [0,1,2]])

for i, b in enumerate(bots):
    dd = dist(b, snb)
    if dd <= snb[3]:
        inrange += 1
print(inrange)

print(mins)
print(maxes)

class Quad:
    def __init__(self, mins, maxes):
        self.mins = mins
        self.maxes = maxes
        self.dims = [self.maxes[i] - self.mins[i] + 1 for i in range(3)]
        self.size = self.dims[0] * self.dims[1] * self.dims[2]
        self.dist = self.dist2point([0,0,0])
        self.num = 0
        for b in bots:
            if self.dist2point(b) <= b[3]:
                self.num += 1

    def dist2point(self, point):
        coords = []
        for c in range(3):
            if point[c] <= self.mins[c]:
                coords += [self.mins[c]]
            elif point[c] >= self.maxes[c]:
                coords += [self.maxes[c]]
            else:
                coords += [point[c]]
        return dist(coords, point)

    def subdivide(self):
        divpoints = [[], [], []]
        for d in range(3):
            if self.dims[d] > 1:
                divpoints[d] += [self.mins[d] + self.dims[d] // 2]
            divpoints[d] += [self.maxes[d]+1]
        mx = self.mins[0]
        for x in divpoints[0]:
            my = self.mins[1]
            for y in divpoints[1]:
                mz = self.mins[2]
                for z in divpoints[2]:
                    yield Quad([mx, my, mz], [x-1, y-1, z-1])
                    mz = z
                my = y
            mx = x

    def __lt__(self, other):
        return (-self.num, self.dist, self.size) < (-other.num, other.dist, other.size)

    def __repr__(self):
        return "[bots {}, dist {}, size {}, [{}, {}, {}], [{}, {}, {}], [{}, {}, {}]]".format(
            self.num, self.dist, self.size, *self.mins, *self.maxes, *self.dims)

#QQ = Quad([57429457, 47789543, 59741497], [57429457, 47789544, 59741498])
#print(QQ)
#for x in QQ.subdivide():
#    print(x)
#sys.exit(0)

heap = []
heapq.heappush(heap, Quad(mins, maxes))

counter = 0
while True:
    q = heapq.heappop(heap)
    counter += 1
    if counter % 10 == 0:
        print(counter, q, len(heap))
    if counter == 1000:
        break
    if q.size == 1:
        print(q)
        break
    for sq in q.subdivide():
        #print(sq)
        if sq.size > 0:
           heapq.heappush(heap, sq)

