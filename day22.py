#!/usr/bin/env python3

depth = 5913
tx, ty = 8, 701

#depth = 510
#tx, ty = 10, 10

level = []
risk = 0

for y in range(ty+1):
    level += [[]]
    for x in range(tx+1):
        if x == 0 and y == 0:
            index = 0
        elif x == tx and y == ty:
            index = 0
        elif y == 0:
            index = x * 16807
        elif x == 0:
            index = y * 48271
        else:
            index = level[y][x-1] * level[y-1][x]
        el = (index + depth) % 20183
        level[y] += [el]
        risk += el % 3

print(risk)