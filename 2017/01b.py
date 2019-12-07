#!/usr/bin/env python3

with open('input01.txt', 'rt') as f:
    ln = f.readline().strip()

sum = 0
stride = len(ln) // 2
for i in range(len(ln)):
    if ln[i-stride] == ln[i]:
        sum += ord(ln[i]) - ord('0')

print(sum)