#!/usr/bin/python3.8

grid = []
pos = {}

with open('input18.txt', 'rt') as f:
    y = 0
    for ln in f.readlines():
        ln = ln.strip()
        for x, c in enumerate(ln):
            if c == '@' or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                pos[c] = (x, y)
        grid += [ln]
        y += 1

def paths_from(what, unlocked):
    p = pos[what]
    q = [(p[0], p[1], 0)]
    qpos = 0
    distances = {}
    visited = set()
    while qpos < len(q):
        x, y, dist = q[qpos]
        qpos += 1
        c = grid[y][x]
        if c == '#' or (x, y) in visited:
            continue
        if c >= 'A' and c <= 'Z' and c not in unlocked:
            continue
        if c >= 'a' and c <= 'z' and c.upper() not in unlocked:
            if c not in distances:
                # found shortest distance to a new key
                distances[c] = dist
        visited.add((x, y))
        for next in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            if next in visited:
                continue
            q += [(next[0], next[1], dist+1)]
    #print(len(q))
    return distances

best = None
minlevel = 15

def recur(start, unlocked, totdist, hops):
    global best
    global minlevel
    if best is not None and totdist > best:
        return best + 1, []
    if len(unlocked) == 26:
        # found last key
        if best is None or totdist < best:
            best = totdist
            print('new best', best)
        return totdist, hops
    mindist = None
    minhops = []
    unlocked.add(start.upper())
    dists = paths_from(start, unlocked)
    for key, dist in dists.items():
        tdist = totdist + dist
        hops += [(key, tdist)]
        s_dist, s_hops = recur(key, unlocked, tdist, hops)
        if mindist is None or s_dist < mindist:
            mindist = s_dist
            minhops = s_hops[:]
        del hops[-1]

    level = len(hops)
    if level < minlevel:
        minlevel = level
        print('new minlevel', minlevel)
    #print(mindist, minhops)
    unlocked.remove(start.upper())
    return mindist, minhops

unlocked = set()
mindist, minhops = recur('@', unlocked, 0, [])
print(mindist)
print(minhops)
