#!/usr/bin/env python3

import curses
import intcode
import sys

with open('input17.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

def input_fn():
    raise "Unexpected input"

grid = ['']

def output_fn(val):
    global grid
    c = chr(val)
    if val == 10:
        if len(grid[-1]) != 0:
            grid += ['']
    else:
        grid[-1] += c


mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)

del grid[-1]

for ln, line in enumerate(grid):
    print(ln, '\t', line)

width = len(grid[0])
height = len(grid)
print(f'width: {width}, height: {height}')

intersect = 0

for y in range(1, height-1):
    for x in range(1, width-1):
        if grid[y][x] != '#':
            continue
        if grid[y-1][x] == '#' and grid[y][x+1] == '#' and grid[y+1][x] == '#' and grid[y][x-1] == '#':
            intersect += x * y

print(intersect)
        