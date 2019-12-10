#!/usr/bin/env python3
import math

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


def angle(other):
    dx = other[0] - station[0]
    dy = station[1] - other[1]
    a = math.atan2(dx, dy)
    if a < 0:
        a += 2 * math.pi
    return (a, dx*dx + dy*dy)


others = [x for x in ast if x != station]
others.sort(key=lambda o: angle(o))

counter = 1
the200 = None
while others:
    prevang = None
    erase = set()
    for o in others:
        ang = angle(o)[0]
        if ang == prevang:
            continue
        prevang = ang
        print("Elim", counter, o)
        if counter == 200:
            the200 = o
        erase.add(o)
        counter += 1
    others = [o for o in others if o not in erase]

print("The 200th one was", the200)
