#!/usr/bin/env python3
import sys
import intcode

with open('input09.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]


def input_fn():
    print('Input')
    line = sys.stdin.readline()
    return int(line)


mach = intcode.IntCode(program)
mach.run(input_fn)
print(f'all outputs: {mach.output}')
