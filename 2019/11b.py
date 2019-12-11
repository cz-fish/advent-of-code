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
minsmaxes = [0,0,0,0]
plate[(0,0)] = 1

def input_fn():
    return plate[(x, y)]

def output_fn(val):
    global moving, x, y, painted, plate, direct, minsmaxes
    if moving:
        # turn left (direct--) or right (direct++)
        direct = (direct + 2*val - 1) % 4
        x, y = {
            0: (x, y-1),
            1: (x+1, y),
            2: (x, y+1),
            3: (x-1, y)
        }[direct]
        minsmaxes = [min(x, minsmaxes[0]), min(y, minsmaxes[1]), max(x, minsmaxes[2]), max(y, minsmaxes[3])]
    else:
        painted.add((x, y))
        plate[(x, y)] = val
    moving = not moving


mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)
print("Painted squares:", len(painted))

width = minsmaxes[2] - minsmaxes[0] + 1
height = minsmaxes[3] - minsmaxes[1] + 1
with open('11-plate.xpm', 'wt') as f:
    f.writelines([
        "! XPM2\n",
        f"{width} {height} 2 1\n",
        "0 c #000000\n",
        "1 c #FFFFFF\n"])
    for row in range(minsmaxes[1], minsmaxes[3]+1):
        line = ''
        for col in range(minsmaxes[0], minsmaxes[2]+1):
            line += str(plate[(col, row)])
        f.write(line + '\n')
        