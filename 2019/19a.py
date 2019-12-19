#!/usr/bin/env python3

import intcode

with open('input19.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

width = 50
height = 50
grid = ['' for i in range(height)]
counter = 0
step = 0

def input_fn():
    global step
    if step == 0:
        step = 1
        return posx
    else:
        step = 0
        return posy


def output_fn(val):
    global grid
    global counter
    if val == 1:
        counter += 1
    grid[posy] += '.#'[val]


for posy in range(height):
    for posx in range(width):
        step = 0
        mach = intcode.IntCode(program)
        mach.run(input_fn, output_fn)

print(counter)
for ln in grid:
    print(ln)

