#!/usr/bin/python3.8

from pyaoc import Input
import re
import sys

inp = Input('input08.txt', ["""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""])

#inp.use_test(0)

program = []
for ln in inp.get_valid_lines():
    instr = ln[:3]
    m = re.search(r'-?\d+', ln)
    assert(m is not None)
    op = int(m.group(0))
    program += [[instr, op]]


def run_prog(prog):
    acc = 0
    pc = 0
    visited = set()
    while True:
        if pc in visited:
            return (False, acc)
        if pc >= len(prog):
            return (True, acc)
        visited.add(pc)
        instr, op = prog[pc]
        if instr == 'nop':
            pc += 1
        elif instr == 'acc':
            acc += op
            pc += 1
        elif instr == 'jmp':
            pc += op

### Part 1

res, acc = run_prog(program)
assert(res == False)
print(f"Part 1: infinite loop accumulator {acc}")

### Part 2

for i in range(len(program)):
    if program[i][0] in ['jmp', 'nop']:
        backup = program[i][0]
        program[i][0] = 'nop' if backup == 'jmp' else 'nop'
        res, acc = run_prog(program)
        if res:
            print(f"Part 2: terminated with acc {acc}")
            sys.exit(0)
        program[i][0] = backup

print("Solution not found")
