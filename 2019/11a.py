#!/usr/bin/env python3

import intcode
from collections import defaultdict

with open('input11.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

x = 0
y = 0
direct = 0
painted = set()
plate = defaultdict(int)
moving = False

def input_fn():
    return plate[(x, y)]

def output_fn(val):
    global moving, x, y, painted, plate, direct
    if moving:
        # turn left (direct--) or right (direct++)
        direct = (direct + 2*val - 1) % 4
        x, y = {
            0: (x, y-1),
            1: (x+1, y),
            2: (x, y+1),
            3: (x-1, y)
        }[direct]
    else:
        painted.add((x, y))
        plate[(x, y)] = val
    moving = not moving


mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)
print("Painted squares:", len(painted))

