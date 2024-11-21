#!/usr/bin/python3.8

from pyaoc import Input

inp = Input('input12.txt', ["""F10
N3
F7
R90
F11
"""])

# inp.use_test(0)

navi = [(ln[0], int(ln[1:])) for ln in inp.get_valid_lines()]
# It seems that L and R values are always multiples of 90

x = 0
y = 0
face = 0
directions = 'ENWS'

for i, a in navi:
    if i == 'F':
        i = directions[face]

    if i == 'E':
        x += a
    elif i == 'N':
        y += a
    elif i == 'W':
        x -= a
    elif i == 'S':
        y -= a
    elif i == 'L':
        s = a // 90
        face = (face + s) % 4
    elif i == 'R':
        s = a // 90
        face = (face - s) % 4

print(f"Part 1: position {x}, {y}, facing {face}, distance {abs(x) + abs(y)}")

# Part 2
wpx = 10
wpy = 1

x = 0
y = 0
face = 0

for i, a in navi:
    if i == 'F':
        x += wpx * a
        y += wpy * a
    elif i == 'E':
        wpx += a
    elif i == 'N':
        wpy += a
    elif i == 'W':
        wpx -= a
    elif i == 'S':
        wpy -= a
    elif i in 'LR':
        s = a // 90
        if i == 'R':
            s = -s
        s = s % 4
        wpx, wpy = [(wpx, wpy), (-wpy, wpx), (-wpx, -wpy), (wpy, -wpx)][s]

print(f"Part 2: position {x}, {y}, facing {face}, distance {abs(x) + abs(y)}")
