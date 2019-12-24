#!/usr/bin/python3.8

grid = []
pos = {}
keys = set()

with open('input18.txt', 'rt') as f:
    y = 0
    for ln in f.readlines():
        ln = ln.strip()
        for x, c in enumerate(ln):
            if c == '@' or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                pos[c] = (x, y)
            if c >= 'a' and c <= 'z':
                keys.add(c)
        grid += [ln]
        y += 1


def paths_from(what):
    p = pos[what]
    q = [(p[0], p[1], 0, '')]
    qpos = 0
    distances = {}
    visited = set()
    while qpos < len(q):
        x, y, dist, doors = q[qpos]
        visited.add((x, y))
        qpos += 1
        c = grid[y][x]
        if c == '#':
            continue
        if c >= 'A' and c <= 'Z':
            for next in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
                if next not in visited:
                    q += [(next[0], next[1], dist+1, doors + c)]
            continue
        if c >= 'a' and c <= 'z':
            key = (c, doors)
            if key not in distances:
                # found shortest distance to a new key
                distances[key] = dist
        for next in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            if next not in visited:
                q += [(next[0], next[1], dist+1, doors)]
    return distances


cross_dist = {}
for start in [k for k in pos.keys() if k in keys or k == '@']:
    paths = paths_from(start)
    cross_dist[start] = {}
    for item, dist in paths.items():
        next_key, doors = item
        cross_dist[start][next_key] = (doors, dist)

best = None
minlevel = 15
hops = [[None, 0] for i in range(len(keys))]


def recur(start, unlocked, tofind, totdist):
    global best
    global minlevel
    global hops

    level = len(unlocked)

    if best is not None and totdist > best:
        return None
    if level == len(keys):
        # found last key
        if best is None or totdist < best:
            best = totdist
            print('new best', best)
        return (totdist, hops)

    mindist = None
    minhops = None
    unlocked.add(start.upper())

    # try to go to each other key that we don't have yet
    dists = cross_dist[start]
    for next_key in tofind:
        doors, dist = dists[next_key]

        locked = False
        for d in doors:
            if d not in unlocked:
                locked = True
                break
        if locked:
            # path from start to next_key is not completely unlocked yet
            continue

        # ok, let's try to go to next_key next
        tdist = totdist + dist
        hops[level][0] = next_key
        hops[level][1] = tdist
        ntofind = set(tofind)
        ntofind.remove(next_key)
        result = recur(next_key, unlocked, ntofind, tdist)
        if result is not None:
            ndist, nhops = result
            if mindist is None or ndist < mindist:
                mindist = ndist
                minhops = nhops[:]

    if level < minlevel:
        minlevel = level
        print('new minlevel', minlevel)

    unlocked.remove(start.upper())
    if mindist is None:
        return None
    return mindist, minhops


unlocked = set()
midist, minhops = recur('@', unlocked, set(keys), 0)
print(mindist)
print(minhops)
