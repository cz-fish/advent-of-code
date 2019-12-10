#!/usr/bin/env python3
import sys

grid = []
with open('input10.txt', 'rt') as f:
    grid += [x.strip() for x in f.readlines()]

height = len(grid)
width = len(grid[0])

ast = []
for y, line in enumerate(grid):
    for x, cel in enumerate(line):
        if cel == '#':
            ast += [(x, y)]

print(width, height)
print("Total asteroids:", len(ast))

best = None
maxvis = 0


def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while a != b:
        s = min(a, b)
        t = max(a, b)
        if s == 0: return t
        a = t-s
        b = s
    return a

for a in ast:
    #print('asteroid', a)
    others = [x for x in ast if x != a]
    others.sort(key=lambda o: abs(o[0]-a[0]) + abs(o[1]-a[1]))
    #print(others)
    obscured = set()
    visible = 0
    for o in others:
        if o in obscured:
            continue
        visible += 1
        x, y = o
        dx = x - a[0]
        dy = y - a[1]
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        x += dx
        y += dy
        #print(x, y, g, dx, dy)
        while x < width and x >= 0 and y < height and y >= 0:
            obscured.add((x, y))
            x += dx
            y += dy
    #print(a, visible, obscured)
    if best is None or visible > maxvis:
        best = a
        maxvis = visible

print(best, maxvis)
