#!/usr/bin/env python3

cnt = 0
for i in range(235741, 706948):
    double = False
    bad = False
    for a in [100000, 10000, 1000, 100, 10]:
        x = (i // a) % 10
        y = (i // (a//10)) % 10
        if y < x:
            bad = True
            break
        elif y == x:
            double = True
    if not bad and double:
        cnt += 1

print(cnt)