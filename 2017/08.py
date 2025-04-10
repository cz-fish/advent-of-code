#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict
from dataclasses import dataclass


e = Env(8)
e.T("""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""", 1, 10)

@dataclass
class Instr:
    reg_update: str
    op: str
    amount: int
    reg_cond: str
    rel_cond: str
    arg_cond: int

def parse_input(input):
    instr = []
    for ln in input.get_valid_lines():
        parts = ln.split(' ')
        reg_u = parts[0]
        op = parts[1]
        assert op in ['inc', 'dec']
        amount = int(parts[2])
        assert parts[3] == 'if'
        reg_c = parts[4]
        rel = parts[5]
        assert rel in ['<', '<=', '>', '>=', '==', '!=']
        arg = int(parts[6])
        instr.append(Instr(reg_u, op, amount, reg_c, rel, arg))
    return instr


def eval_condition(a, op, b):
    if op == '<':
        return a < b
    elif op == '<=':
        return a <= b
    elif op == '>':
        return a > b
    elif op == '>=':
        return a >= b
    elif op == '==':
        return a == b
    elif op == '!=':
        return a != b
    assert False


def run(instr, regs):
    intermediate_max = 0
    for i in instr:
        test = regs[i.reg_cond]
        if eval_condition(test, i.rel_cond, i.arg_cond):
            amt = i.amount
            if i.op == 'dec':
                amt = -amt
            regs[i.reg_update] += amt
            intermediate_max = max(intermediate_max, regs[i.reg_update])
    return intermediate_max


def part1(input):
    instr = parse_input(input)
    regs = defaultdict(int)
    run(instr, regs)
    return max(regs.values())


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    instr = parse_input(input)
    regs = defaultdict(int)
    return run(instr, regs)


e.run_tests(2, part2)
e.run_main(2, part2)
