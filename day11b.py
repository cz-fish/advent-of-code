#!/usr/bin/env python3

#serial = 18
#serial = 42
serial = 2568

def make_grid(serial):
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
    return power

def solve(power, square):
    pow = 0
    for y in range(square):
        pow += sum(power[y][:square])
    bestx = 0
    besty = 0
    best = pow
    prow = pow

    for y in range(square-1,300):
        if y >= square:
            pow = prow
            pow += sum(power[y][:square]) - sum(power[y-square][:square])
            prow = pow

        for x in range(square-1,300):
            if x >= square:
                for v in range(square):
                    pow += power[y-v][x] - power[y-v][x-square]
            if pow > best:
                best = pow
                bestx = x - square+1
                besty = y - square+1
    return best, bestx, besty

power = make_grid(serial)

global_best = None

print(solve(power, 3))

for square in range(2,301):
    best, bestx, besty = solve(power, square)
    if global_best is None or best > global_best[0]:
        global_best = [best, bestx, besty, square]
    print(square, global_best)

print()
print(global_best)

#for y in range(besty-1,besty+4):
#    print (power[y][bestx-1:bestx+4])
