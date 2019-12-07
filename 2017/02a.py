#!/usr/bin/env python3

grid = []
with open('input02.txt', 'rt') as f:
    for ln in f.readlines():
        grid.append([int(x) for x in ln.strip().split('\t')])

print(sum([max(l) - min(l) for l in grid]))

print('-----')

s = 0
for ln in grid:
    srt = sorted(ln)
    stop = False
    for i in range(len(srt) - 1):
        x = srt[i]
        if x == 0:
            continue
        for j in range(i+1, len(srt)):
            y = srt[j]
            if y // x * x == y:
                s += y // x
                stop = True
                break
        if stop:
            break

print(s)