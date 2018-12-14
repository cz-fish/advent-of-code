#!/usr/bin/env python3

import re

inp = []

with open('day4.txt', 'rt') as f:
    inp = [x.strip() for x in f.readlines()]

inp.sort()

guards = {}
current = None
slept = None

maxminute = 0
maxguard = None

for ev in inp:
    m = re.match(r'^\[1518-(\d\d)-(\d\d) (\d\d):(\d\d)\] (.*)', ev)
    if not m:
        print('doesn\'t match: ', format(ev))
    _d, _m, _h, _mm, what = m.groups()
    day = int(_d)
    month = int(_m)
    hour = int(_h)
    minute = int(_mm)

    if what == 'wakes up':
        if slept is None:
            print('wakes up without sleeping: ', ev)
            continue
        if current is None:
            print('wakes up, no guard: ', ev)
            continue
        if current not in guards:
            guards[current] = [[0,0], [0]*60]
        g = guards[current]
        for i in range(slept, minute):
            g[1][i] += 1
            if g[1][i] > g[0][0]:
                g[0][0] = g[1][i]
                g[0][1] = i
        if g[0][0] > maxminute:
            maxminute = g[0][0]
            maxguard = current
        slept = None

    elif what == 'falls asleep':
        if current is None:
            print('falls asleep, no guard: ', ev)
            continue
        slept = minute

    elif what.startswith('Guard '):
        mm = re.search(r'Guard #(\d+) begins', what)
        if not mm:
            print('no match: ', what, ' -- ', ev)
            continue
        current = int(mm.groups()[0])

g = guards[maxguard]

print('{} {} - {}'.format(maxguard, g[0][1], maxguard * g[0][1]))