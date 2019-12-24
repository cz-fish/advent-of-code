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
    cross_dist[start] = paths_from(start)
    # for k, v in cross_dist[start].items():
    #     print(start, k, v)

best = None
minlevel = 15


def recur(start, unlocked, totdist, hops):
    global best
    global minlevel
    if best is not None and totdist > best:
        return best + 1, []
    if len(unlocked) == len(keys):
        # found last key
        if best is None or totdist < best:
            best = totdist
            print('new best', best)
        return totdist, hops

    mindist = None
    minhops = []
    unlocked.add(start.upper())

    # try to go to each other key that we don't have yet
    dists = cross_dist[start]
    for item, dist in dists.items():
        next_key, doors = item
        if next_key.upper() in unlocked:
            # we already have next_key, skip
            continue

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
        hops += [(next_key, tdist)]
        s_dist, s_hops = recur(next_key, unlocked, tdist, hops)
        if mindist is None or s_dist < mindist:
            mindist = s_dist
            minhops = s_hops[:]
        del hops[-1]

    level = len(hops)
    if level < minlevel:
        minlevel = level
        print('new minlevel', minlevel)

    unlocked.remove(start.upper())
    return mindist, minhops


unlocked = set()
midist, minhops = recur('@', unlocked, 0, [])
print(mindist)
print(minhops)
