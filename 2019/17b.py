#!/usr/bin/env python3

import intcode

with open('input17.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]
program[0] = 2

input_lines = [
    'A,B,A,B,C,C,B,A,C,A\n',
    'L,10,R,8,R,6,R,10\n',
    'L,12,R,8,L,12\n',
    'L,10,R,8,R,8\n',
    'n\n'
]

input = [ord(c) for c in ''.join(input_lines)]
pos = 0


def input_fn():
    global pos
    v = input[pos]
    pos += 1
    return v


mach = intcode.IntCode(program)
mach.run(input_fn)

print(f'Dust collected: {mach.output[-1]}')
