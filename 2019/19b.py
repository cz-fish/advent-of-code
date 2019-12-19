#!/usr/bin/env python3

import intcode

with open('input19.txt', 'rt') as f:
    lines = f.readline().strip()
program = [int(i) for i in lines.split(',')]

step = 0


def input_fn(xy):
    global step
    if step == 0:
        step = 1
        return xy[0]
    else:
        step = 0
        return xy[1]


def test(x, y):
    mach = intcode.IntCode(program)
    mach.run(lambda: input_fn([x, y]))
    return mach.output[-1]


height = 300
left = 350
top = 920


def find_if(y, minleft, lookfor):
    x = minleft
    while True:
        v = test(x, y)
        if v == lookfor:
            return x
        x += 1


for posy in range(top, top+height):
    line1left = find_if(posy, left, 1)
    left = line1left
    line1right = find_if(posy, line1left + 1, 0)

    line2left = find_if(posy + 99, line1left, 1)
    square_width = line1right - line2left
    print(f'line {posy}, left {line1left}, right {line1right}, botline {posy+99}, left {line2left}, square {square_width}')
    if square_width >= 100:
        print('result', line2left * 10000 + posy)
        break

