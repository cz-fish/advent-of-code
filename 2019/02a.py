#!/usr/bin/env python3

with open('input02.txt', 'rt') as f:
    l = f.readline().strip()

mem = [int(i) for i in l.split(',')]

mem[1] = 12
mem[2] = 2

pos = 0
while True:
    op = mem[pos]
    if op == 99:
        break
    a = mem[mem[pos+1]]
    b = mem[mem[pos+2]]
    d = mem[pos+3]
    if op == 1:
        r = a + b
    elif op == 2:
        r = a * b
    mem[d] = r
    pos += 4

print(mem[0])
