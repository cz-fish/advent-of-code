#!/usr/bin/env python3

tree = {}
parents = {}

with open('input06.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        a, b = tuple(ln.split(')'))
        if a not in tree:
            tree[a] = []
        tree[a] += [b]
        parents[b] = a

node = 'YOU'
path = {}
counter = -1
while node != 'COM':
    path[node] = counter
    counter += 1
    node = parents[node]

#print(path)

node = 'SAN'
counter = -1
while node != 'COM':
    if node in path:
        print(counter + path[node])
        break
    counter += 1
    node = parents[node]

