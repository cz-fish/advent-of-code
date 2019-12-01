#!/usr/bin/env python3

with open('input01.txt', 'rt') as f:
    input = [int(x) for x in f.readlines()]

total = 0

for i in input:
    rem = max(0, (i//3)-2)
    total += rem

    while rem > 0:
        rem = max((rem//3)-2,0)
        total += rem

print(total)