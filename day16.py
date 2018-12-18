#!/usr/bin/env python3

samples = []
with open('inputs/day16.txt', 'rt') as f:
    while True:
        b = f.readline().strip()
        if not b:
            break
        o = f.readline().strip()
        a = f.readline().strip()
        f.readline()

        before = [int(i) for i in b[9:-1].split(',')]
        op = [int(i) for i in o.split(' ')]
        after = [int(i) for i in a[9:-1].split(',')]
        samples += [(before, op, after)]
        
        
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

all = [
    addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
]

#samples = [([3,2,1,1], [9,2,1,2], [3,2,2,1])]
cntr = 0
for s in samples:
    pos = 0
    for o in all:
        r = s[0][:]
        o(*s[1][1:], r)
        #print(o.__name__, r)
        if r == s[2]:
            pos += 1
    if pos >= 3:
        cntr += 1

print(cntr)