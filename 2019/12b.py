#!/usr/bin/python3.8
import re
from numpy import lcm

positions = []
with open('input12.txt', 'rt') as f:
    for moonline in f.readlines():
        m = re.findall(r'-?\d+', moonline)
        positions += [[int(c) for c in m]]

nmoons = len(positions)

def one_step(pos, vel):
    # update velocities
    nvel = vel[:]
    for i in range(nmoons):
        for j in range(i, nmoons):
            d = pos[i] - pos[j]
            if d < 0:
                nvel[i] += 1
                nvel[j] -= 1
            elif d > 0:
                nvel[i] -= 1
                nvel[j] += 1
    
    # update positions
    npos = [pos[i] + nvel[i] for i in range(nmoons)]
    return npos, nvel

def key(pos, vel):
    return '{},{},{};{},{},{}'.format(*pos, *vel)

periods = []
for dim in [0,1,2]:
    counter = 0
    pos = [positions[i][dim] for i in range(nmoons)]
    vel = [0] * nmoons
    initkey = key(pos, vel)
    #vis = {initkey: 0}
    while True:
        pos, vel = one_step(pos, vel)
        counter += 1
        k = key(pos, vel)
        if k == initkey:
            #if k in vis:
            periods += [(counter, pos, vel)]
            break
        #vis[k] = counter

print(periods)
period = lcm.reduce([p[0] for p in periods])
print(period)