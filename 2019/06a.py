#!/usr/bin/env python3

tree = {}

with open('input06.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        a, b = tuple(ln.split(')'))
        if a not in tree:
            tree[a] = []
        tree[a] += [b]

orbits = 0
q = [('COM', 0)]
qi = 0

while qi < len(q):
    node, depth = q[qi]
    qi += 1
    orbits += depth
    if node not in tree:
        continue
    for c in tree[node]:
        q += [(c, depth + 1)]

print(orbits)

