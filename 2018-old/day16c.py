#!/usr/bin/env python3

program = []
with open('inputs/day16.txt', 'rt') as f:
    while True:
        b = f.readline().strip()
        if not b:
            break
        f.readline()
        f.readline()
        f.readline()

    f.readline()
    while True:
        ll = f.readline().strip()
        if not ll: break
        program += [[int(i) for i in ll.split(' ')]]


def addr(a, b, c, regs):
    regs[c] = regs[a] + regs[b]

def addi(a, b, c, regs):
    regs[c] = regs[a] + b

def mulr(a, b, c, regs):
    regs[c] = regs[a] * regs[b]

def muli(a, b, c, regs):
    regs[c] = regs[a] * b

def banr(a, b, c, regs):
    regs[c] = regs[a] & regs[b]

def bani(a, b, c, regs):
    regs[c] = regs[a] & b

def borr(a, b, c, regs):
    regs[c] = regs[a] | regs[b]

def bori(a, b, c, regs):
    regs[c] = regs[a] | b

def setr(a, b, c, regs):
    regs[c] = regs[a]

def seti(a, b, c, regs):
    regs[c] = a

def gtir(a, b, c, regs):
    regs[c] = [0,1][a > regs[b]]

def gtri(a, b, c, regs):
    regs[c] = [0,1][regs[a] > b]

def gtrr(a, b, c, regs):
    regs[c] = [0,1][regs[a] > regs[b]]

def eqir(a, b, c, regs):
    regs[c] = [0,1][a == regs[b]]

def eqri(a, b, c, regs):
    regs[c] = [0,1][regs[a] == b]

def eqrr(a, b, c, regs):
    regs[c] = [0,1][regs[a] == regs[b]]

opmap = {
    0: bani,
    1: addr,
    2: mulr,
    3: addi,
    4: gtri,
    5: banr,
    6: borr,
    7: eqri,
    8: seti,
    9: eqrr,
    10: bori,
    11: setr,
    12: eqir,
    13: muli,
    14: gtrr,
    15: gtir
}

regs = [0,0,0,0]

for i in program:
    opmap[i[0]](i[1], i[2], i[3], regs)

print(regs)
