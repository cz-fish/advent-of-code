#!/usr/bin/env python3

import queue

ipreg = 0
program = {}
icntr = 0
with open('inputs/day19.txt', 'rt') as f:
    while True:
        b = f.readline().strip()
        if not b:
            break
        if b.startswith('#ip '):
            ipreg = int(b[3:])
        else:
            p = b.split(' ')
            program[icntr] = (p[0], int(p[1]), int(p[2]), int(p[3]))
            icntr += 1


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

#regs = [0,0,0,0,0,0]
regs = [1,0,0,0,0,0]

pc = 0
ip = 0
#run = queue.Queue()

while ip in program:
    pc += 1
    if pc == 100: break
    instr = program[ip]
    oregs = regs[:]
    globals()[instr[0]](instr[1], instr[2], instr[3], regs)
    #run.put("{:4} {:2} {:35} {:20} {:35}".format(pc, ip, str(oregs), str(instr), str(regs)))
    #if run.qsize() > 20: run.get()
    print("{:4} {:2} {:35} {:20} {:35}".format(pc, ip, str(oregs), str(instr), str(regs)))
    ip = regs[ipreg]
    ip += 1
    regs[ipreg] = ip

print(regs)

#while not run.empty():
#    print(run.get())

