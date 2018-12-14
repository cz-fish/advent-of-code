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

time = 0
workers = [None] * 5
allFree = True

while heads or not allFree:
    print (time, workers)
    firstFree = None
    allFree = True
    for i in range(5):
        if workers[i] is not None and workers[i][1] == time:
            # job n is done
            n = workers[i][0]
            if n in g:
                for nn in g[n]:
                    req[nn].remove(n)
                    if not req[nn]:
                        heads.add(nn)
            # worker is free
            workers[i] = None

        if workers[i] is None:
            if firstFree is None:
                firstFree = i
        else:
            allFree = False
    
    if firstFree is None:
        # no free worker, wait 1 time unit
        time += 1
        continue

    if heads:
        # firstFree worker takes the first job
        v = list(heads)
        v.sort()
        p = v[0]
        tasktime = 61 + ord(p) - ord('A')
        finish = time + tasktime
        workers[firstFree] = (p, finish)
        heads.remove(p)
        allFree = False
    elif not allFree:
        time += 1


print(time)

