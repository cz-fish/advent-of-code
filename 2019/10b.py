#!/usr/bin/env python3
import math
import sys

grid = []
with open('input10.txt', 'rt') as f:
    grid += [x.strip() for x in f.readlines()]

height = len(grid)
width = len(grid[0])

station = (26, 29)
#station = (8, 3)
#station = (11,13)

ast = []
for y, line in enumerate(grid):
    for x, cel in enumerate(line):
        if cel == '#':
            ast += [(x, y)]

print(width, height)
print("Total asteroids:", len(ast))

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

others = [x for x in ast if x != station]
others.sort(key=lambda o: abs(o[0]-station[0]) + abs(o[1]-station[1]))
obscured = set()

def get_line(other):
    if other in obscured:
        return
    x, y = other
    dx = x - station[0]
    dy = y - station[1]
    g = gcd(dx, dy)
    dx //= g
    dy //= g
    x += dx
    y += dy
    while x < width and x >= 0 and y < height and y >= 0:
        yield (x, y)
        x += dx
        y += dy


for o in others:
    for x in get_line(o):
        obscured.add(x)


def angle(other):
    dx = other[0] - station[0]
    dy = station[1] - other[1]
    a = math.atan2(dx, dy)
    if a < 0:
        a += 2 * math.pi
    return (a, dx*dx + dy*dy)

others.sort(key=lambda o: angle(o))
#for o in others:
#    print(o, angle(o))

counter = 1
while others:
    prevang = None
    erase = set()
    for o in others:
        ang = angle(o)[0]
        if ang == prevang:
            continue
        prevang = ang
        print("Elim", counter, o)
        erase.add(o)
        counter += 1
    others = [o for o in others if o not in erase]

