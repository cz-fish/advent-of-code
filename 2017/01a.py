#!/usr/bin/env python3

with open('input01.txt', 'rt') as f:
    ln = f.readline().strip()

sum = 0
for i in range(len(ln)):
    if ln[i-1] == ln[i]:
        sum += ord(ln[i]) - ord('0')

print(sum)