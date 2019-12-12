#!/usr/bin/env python3
import re

maxiter = 1000

positions = []
with open('input12.txt', 'rt') as f:
    for moonline in f.readlines():
        m = re.findall(r'-?\d+', moonline)
        positions += [[int(c) for c in m]]

nmoons = len(positions)
velocities = [[0,0,0] for p in range(nmoons)]

def one_step(pos, vel):
    # update velocities
    nvel = [vel[p][:] for p in range(nmoons)]
    for i in range(nmoons):
        x = pos[i]
        for j in range(i, nmoons):
            y = pos[j]
            for dim in [0,1,2]:
                d = x[dim] - y[dim]
                if d < 0:
                    nvel[i][dim] += 1
                    nvel[j][dim] -= 1
                elif d > 0:
                    nvel[i][dim] -= 1
                    nvel[j][dim] += 1
    
    # update positions
    npos = []
    nsta = []
    nkin = []
    ntot = []
    for i in range(nmoons):
        npos += [
            [pos[i][d] + nvel[i][d] for d in [0,1,2]]
        ]
        nsta += [
            sum([abs(npos[i][d]) for d in [0,1,2]])
        ]
        nkin += [
            sum([abs(nvel[i][d]) for d in [0,1,2]])
        ]
        ntot += [nsta[i] * nkin[i]]
    
    return npos, nvel, nsta, nkin, ntot


for i in range(1, maxiter + 1):
    pos, vel, sta, kin, tot = one_step(positions, velocities)
    print(f'i={i}, pos={pos}, vel={vel}')
    if i == maxiter:
        print(f'sta={sta}, kin={kin}, tot={tot}, res={sum(tot)}')
    positions = pos
    velocities = vel

