#!/usr/bin/python3.12

from pyaoc import Env
from dataclasses import dataclass


e = Env(23)
e.T("""inc a
jio a, +2
tpl a
inc a""", 0, None)


@dataclass
class Instr:
    type: str
    arg0: int
    arg1: int



def read_program(input):
    program = []
    for ln in input.get_valid_lines():
        mnemo = ln[:3]
        assert mnemo in ['hlf', 'tpl', 'inc', 'jmp', 'jie', 'jio']
        params = ln[4:].split(", ")
        arg1 = 0 if len(params) == 1 else int(params[1])
        if mnemo == 'jmp':
            arg0 = int(params[0])
        else:
            assert params[0] in ['a', 'b']
            arg0 = 0 if params[0] == 'a' else 1
        program.append(Instr(mnemo, arg0, arg1))
    return program


def run_program(program, a, b):
    ip = 0
    regs = [a, b]
    while ip < len(program):
        i = program[ip]
        if i.type == "hlf":
            regs[i.arg0] = regs[i.arg0] // 2
            ip += 1
        elif i.type == "tpl":
            regs[i.arg0] = regs[i.arg0] * 3
            ip += 1
        elif i.type == "inc":
            regs[i.arg0] = regs[i.arg0] + 1
            ip += 1
        elif i.type == "jmp":
            ip += i.arg0
        elif i.type == "jie":
            if regs[i.arg0] % 2 == 0:
                ip += i.arg1
            else:
                ip += 1
        elif i.type == "jio":
            if regs[i.arg0] == 1:
                ip += i.arg1
            else:
                ip += 1
    return regs[0], regs[1]


def part1(input):
    program = read_program(input)
    a, b = run_program(program, 0, 0)
    return b


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    program = read_program(input)
    a, b = run_program(program, 1, 0)
    return b


# e.run_tests(2, part2)
e.run_main(2, part2)
