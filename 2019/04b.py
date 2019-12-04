#!/usr/bin/env python3

cnt = 0
for i in range(235741, 706948):
    dig = [int(c) for c in str(i)]
    double = False
    bad = False
    run = 1
    for a in range(1,6):
        x = dig[a-1]
        y = dig[a]
        if y < x:
            bad = True
            break
        elif y == x:
            run += 1
        else:
            if run == 2:
                double = True
            run = 1
    if not bad and (double or run == 2):
        cnt += 1

print(cnt)