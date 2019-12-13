#!/usr/bin/env python3

import intcode

with open('input13.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

def input_fn():
    pass

def get_blocks(output):
    count = 0
    for i in range(0,len(output),3):
        print(output[i:i+3])
        if output[i+2] == 2:
            count += 1
    return count

mach = intcode.IntCode(program)
mach.run(input_fn)
blocks = get_blocks(mach.output)

print("Block tiles:", blocks)
