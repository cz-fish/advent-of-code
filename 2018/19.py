#!/usr/bin/python3.8

from aoc import Env
from wristwatch import WristwatchComputer

e = Env(19)
e.T("""#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""", 6, 6)


def parse_program(input):
    ip = None
    program = []
    for ln in input.get_valid_lines():
        if ln.startswith('#ip '):
            assert ip is None, f"instruction pointer given twice - previous {ip}, now {ln}"
            ip = int(ln[4:])
        else:
            parts = ln.split(' ')
            assert len(parts) == 4, f"wrong instruction format {ln}"
            program.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    assert ip is not None, "Expected instruction pointer declaration, but didn't find it!"
    return ip, program


def part1(input):
    ip, program = parse_program(input)
    comp = WristwatchComputer(ip)
    comp.run(program, False, None)
    return comp.reg[0]


e.run_tests(1, part1)
e.run_main(1, part1)

"""
tail of part 1

6297703 5       [888, 0, 887, 887, 5, 887]      ('addr', 1, 4, 4)       [888, 0, 887, 887, 5, 887]
6297704 6       [888, 0, 887, 887, 6, 887]      ('addi', 4, 1, 4)       [888, 0, 887, 887, 7, 887]
6297705 8       [888, 0, 887, 887, 8, 887]      ('addi', 5, 1, 5)       [888, 0, 887, 887, 8, 888]
6297706 9       [888, 0, 887, 887, 9, 888]      ('gtrr', 5, 2, 1)       [888, 1, 887, 887, 9, 888]
6297707 10      [888, 1, 887, 887, 10, 888]     ('addr', 4, 1, 4)       [888, 1, 887, 887, 11, 888]
6297708 12      [888, 1, 887, 887, 12, 888]     ('addi', 3, 1, 3)       [888, 1, 887, 888, 12, 888]
6297709 13      [888, 1, 887, 888, 13, 888]     ('gtrr', 3, 2, 1)       [888, 1, 887, 888, 13, 888]
6297710 14      [888, 1, 887, 888, 14, 888]     ('addr', 1, 4, 4)       [888, 1, 887, 888, 15, 888]
6297711 16      [888, 1, 887, 888, 16, 888]     ('mulr', 4, 4, 4)       [888, 1, 887, 888, 256, 888]
Day 19 Part 1: 888
"""

def part2(input):
    ip, program = parse_program(input)
    comp = WristwatchComputer(ip)
    comp.reg[0] = 1
    for expl in comp.explain_program(program):
        print(expl)
    #comp.run(program, True)
    #return comp.reg[0]

e.run_tests(2, part2)
e.run_main(2, part2)

# 10551288 too low
