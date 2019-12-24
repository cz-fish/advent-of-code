#!/usr/bin/python3.8

grid = []

with open('input24.txt', 'rt') as f:
    for ln in f.readlines():
        grid += [ln.strip()]

def biodiv(grid):
    bd = 0
    pow = 0
    for ln in grid:
        for i, c in enumerate(ln):
            if c == '#':
                bd += 2 ** (pow + i)
        pow += 5
    return bd

def next_minute(grid):
    ngrid = []
    for y in range(5):
        ngrid += ['']
        for x in range(5):
            nei = ''
            if x > 0:
                nei += grid[y][x-1]
            if x < 4:
                nei += grid[y][x+1]
            if y > 0:
                nei += grid[y-1][x]
            if y < 4:
                nei += grid[y+1][x]
            c = grid[y][x]
            bugs = nei.count('#')
            if c == '#' and bugs != 1:
                c = '.'
            elif c == '.' and (bugs == 1 or bugs == 2):
                c = '#'
            ngrid[-1] += c
    return ngrid

diversities = set()
bd = biodiv(grid)
diversities.add(bd)

while True:
    grid = next_minute(grid)
    bd = biodiv(grid)
    if bd in diversities:
        print('Biodiversity spotted twice', bd)
        break
    diversities.add(bd)
