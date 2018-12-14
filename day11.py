#!/usr/bin/env python3

#serial = 18
#serial = 42
serial = 2568

power = []
for y in range(300):
    power += [[]]
    for x in range(300):
        rackid = x + 10
        powerstart = rackid * y + serial
        p = powerstart * rackid
        hundreds = (p // 100) % 10
        v = hundreds - 5
        power[y] += [v]

pow = sum(power[0][:3]) + sum(power[1][:3]) + sum(power[2][:3])
bestx = 0
besty = 0
best = pow
prow = pow

for y in range(2,300):
    if y > 2:
        pow = prow
        pow += power[y][0] + power[y][1] + power[y][2] - \
            (power[y-3][0] + power[y-3][1] + power[y-3][2])
        prow = pow

    for x in range(2,300):
        if x > 2:
            pow += power[y][x] + power[y-1][x] + power[y-2][x] - \
                (power[y][x-3] + power[y-1][x-3] + power[y-2][x-3])
        if pow > best:
            best = pow
            bestx = x - 2
            besty = y - 2

print(best, bestx, besty)

for y in range(besty-1,besty+4):
    print (power[y][bestx-1:bestx+4])
