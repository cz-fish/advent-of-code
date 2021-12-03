#!/usr/bin/env python3

import queue

pts = []
with open('inputs/day25a.txt', 'rt') as f:
    for ll in f.readlines():
        v = [int(i) for i in ll.split(',')]
        pts += [v]

minmax = []
for i in range(4):
    mm = None
    MM = None
    for x in pts:
        if mm is None or x[i] < mm:
            mm = x[i]
        if MM is None or x[i] > MM:
            MM = x[i]
    minmax += [(mm, MM)]

print(minmax)

def dist(a, b):
    return sum([abs(a[i]-b[i]) for i in [0,1,2,3]])

groups = {}

for i, p in enumerate(pts):
    for j in range(i+1, len(pts)):
        d = dist(p, pts[j])
        if d <= 3:
            if i not in groups:
                groups[i] = set()
            groups[i].add(j)
            if j not in groups:
                groups[j] = set()
            groups[j].add(i)

visited = set()
const = []
for i in range(len(pts)):
    if i in visited:
        continue
    visited.add(i)
    const += [[i]]
    if i not in groups:
        continue
    q = queue.Queue()
    for x in groups[i]:
        q.put(x)
    while not q.empty():
        j = q.get()
        if j in visited:
            continue
        visited.add(j)
        const[-1] += [j]
        if j in groups:
            for x in groups[j]:
                q.put(x)

print(len(const))
