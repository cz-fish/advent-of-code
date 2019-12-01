#!/usr/bin/env python3

with open('input01.txt', 'rt') as f:
    input = [int(x) for x in f.readlines()]

total = sum([(i//3)-2 for i in input])
print(total)