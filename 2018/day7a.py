#!/usr/bin/env python3


import re


heads = set()
g = {}
req = {}


seen = set()
with open('day7.txt', 'rt') as f:
    for l in f.readlines():
        s, e = re.match(r'^Step (.).*step (.)', l).groups()
        
        if s not in g:
            g[s] = []
        g[s] += [e]
        
        if e not in req:
            req[e] = set()
        req[e].add(s)


        if e in heads:
            heads.remove(e)
        if s not in seen:
            heads.add(s)
        seen.add(s)
        seen.add(e)


print(g)
print(heads)


out = ''
while heads:
    v = list(heads)
    v.sort()
    p = v[0]
    out += p
    if p in g:
        for i in g[p]:
            req[i].remove(p)
            if not req[i]:
                heads.add(i)
    heads.remove(p)


print(out)