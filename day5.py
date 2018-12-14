#!/usr/bin/env python3

pol = ''

with open('day5.txt', 'rt') as f:
    pol = f.readline().strip()

def match(a, b):
    return a != b and a.upper() == b.upper()

def react(pol):
    ll = len(pol)
    skip = [0] * ll

    prev = None
    prev_i = None
    i = -1

    while True:
        i += 1
        while (i < ll and skip[i] == 1):
            i += 1
        if i == ll: break

        if prev is None:
            prev = pol[i]
            prev_i = i
            continue
        
        if match(prev, pol[i]):
            skip[prev_i] = 1
            skip[i] = 1
            i = prev_i - 1
            prev = None
            while (i >= 0 and skip[i] == 1):
                i -= 1
            if i >= 0:
                i -= 1
        else:
            prev = pol[i]
            prev_i = i

    return ll - sum(skip)

print(react(pol))
