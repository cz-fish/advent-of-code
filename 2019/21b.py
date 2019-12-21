#!/usr/bin/env python3

import intcode

with open('input21.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

# (!A) || (!C && D && H) || (!B && D)
input_lines = [
    'NOT C J\n',
    'AND D J\n',
    'AND H J\n',
    'NOT A T\n',
    'OR T J\n',
    'NOT B T\n',
    'AND D T\n',
    'OR T J\n',
    'RUN\n'
]

input = [ord(c) for c in ''.join(input_lines)]
pos = 0


def input_fn():
    global pos
    v = input[pos]
    pos += 1
    return v

def output_fn(val):
    if val > 255:
        print(val)
    else:
        print(chr(val), end='')


mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)

print()
