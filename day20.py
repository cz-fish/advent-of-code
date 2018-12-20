#!/usr/bin/env python3

import queue

with open('inputs/day20.txt', 'rt') as f:
    rex = f.readline().strip()[1:-1]

minx = 200
maxx = 200
miny = 200
maxy = 200
dist_map = {}

def door(mm, x, y, c):
    if mm[y][x] in ' ?':
        mm[y][x] = c

def room(map, x, y, doors, dist):
    global dist_map
    if (x,y) not in dist_map or dist < dist_map[(x,y)]:
        dist_map[(x,y)] = dist
    mm[y][x] = '.'
    mm[y-1][x-1] = '#'
    mm[y-1][x+1] = '#'
    mm[y+1][x-1] = '#'
    mm[y+1][x+1] = '#'
    door(mm, x-1, y, '?|'['W' in doors])
    door(mm, x+1, y, '?|'['E' in doors])
    door(mm, x, y-1, '?-'['N' in doors])
    door(mm, x, y+1, '?-'['S' in doors])

def fix_walls(mm):
    for y in range(miny-1, maxy+2):
        for x in range(minx-1, maxx+2):
            if mm[y][x] == '?':
                mm[y][x] = '#'

def print_map(mm):
    for y in range(miny-1, maxy+2):
        print(''.join(mm[y][minx-1:maxx+2]))

mm = []
for y in range(400):
    mm += [[]]
    mm[y] = [' ' for x in range(400)]

x = minx
y = miny
room(mm, x, y, '', 0)
mm[y][x] = 'X'

steps = {
    'E': (2, 0, 'W'),
    'W': (-2, 0, 'E'),
    'N': (0, -2, 'S'),
    'S': (0, 2, 'N')
}

starts = []

dist = 0
for i, c in enumerate(rex):
    if c in 'EWNS':
        dist += 1
        st = steps[c]
        x += st[0]
        y += st[1]
        room(mm, x, y, st[2], dist)
        if x < minx: minx = x
        if x > maxx: maxx = x
        if y < miny: miny = y
        if y > maxy: maxy = y
    elif c == '(':
        starts += [(x, y, dist)]
    elif c == '|':
        x, y, dist = starts[-1]
    elif c == ')':
        starts.pop()

fix_walls(mm)
print_map(mm)

print(minx, maxx, miny, maxy)

max_dist = None
over1000 = 0
for p, dist in dist_map.items():
    if max_dist is None or dist > max_dist[1]:
        max_dist = (p, dist)
    if dist >= 1000:
        over1000 += 1

print(max_dist)
print(over1000)