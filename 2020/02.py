#!/usr/bin/python3.8

import re
from collections import namedtuple

Policy = namedtuple('Policy', ['minc', 'maxc', 'char'])

pwds = []
pattern = re.compile(r'^(\d+)-(\d+) (.): (.*)')
with open('input02.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        m = pattern.match(ln)
        assert(m is not None)
        pwds += [(Policy(
            minc=int(m.group(1)),
            maxc=int(m.group(2)),
            char=m.group(3)),
            m.group(4))]

good_count = 0
for pol, pwd in pwds:
    t = pwd.count(pol.char)
    if t >= pol.minc and t <= pol.maxc:
        good_count += 1

print(f"Part 1: Good passwrods: {good_count}")

good_count = 0
for pol, pwd in pwds:
    t = sum([pwd[pol.minc-1] == pol.char, pwd[pol.maxc-1] == pol.char])
    if t == 1:
        good_count += 1

print(f"Part 2: Good passwrods: {good_count}")
