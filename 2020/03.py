#!/usr/bin/python3.8

from collections import namedtuple
from functools import reduce

Slope = namedtuple('Slope', ['x', 'y'])

forest = []
with open('input03.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        if not ln:
            continue
        forest += [ln]


def count_trees(slope):
    x = 0
    y = 0
    trees = 0
    fw = len(forest[0])
    fh = len(forest)
    while y < fh:
        if forest[y][x % fw] == '#':
            trees += 1
        x += slope.x
        y += slope.y
    return trees


# Part 1
print(f"Part 1, trees on path: {count_trees(Slope(3, 1))}")

# Part 2
results = []
for slope in [Slope(1,1), Slope(3,1), Slope(5,1), Slope(7, 1), Slope(1,2)]:
    results += [count_trees(slope)]

print(f"Part 2, results: {results}, multiplied: {reduce(lambda x, y: x*y, results)}")
