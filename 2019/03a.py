#!/usr/bin/env python3

with open('input03.txt', 'rt') as f:
    wires = [s.strip() for s in f.readlines()]

#wires = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
#wires = ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']
#wires = ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']

wires = [s.split(',') for s in wires[:2]]

def trace(wire):
    x = 0
    y = 0
    pos = set()
    for tok in wire:
        d = {'R': (1,0), 'U': (0,1), 'L': (-1,0), 'D': (0,-1)}[tok[0]]
        amp = int(tok[1:])
        while amp > 0:
            x += d[0]
            y += d[1]
            k = f'{x},{y}'
            pos.add(k)
            amp -= 1
    return pos


first = trace(wires[0])
second = trace(wires[1])

crosses = first.intersection(second)

def dist(pt):
    x, y = pt.split(',')
    return abs(int(x)) + abs(int(y))

print(sorted([dist(pt) for pt in crosses]))
