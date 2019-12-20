#!/usr/bin/python3.8

with open('input20.txt', 'rt') as f:
    lines = [ln[:-1] for ln in f.readlines()]

## outer border
# assume that there is always a portal at the top
donut_top = 2
# assume there is always a portal on the left
donut_left = 2
# assume there is always portal at the bottom
donut_bottom = len(lines) - 3
donut_right = lines[donut_top].rfind('#')

## inner border
inner_top = donut_bottom
inner_left = donut_right
inner_right = donut_left
inner_bottom = donut_top
for i in range(donut_top+1, donut_bottom):
    middle = lines[i][donut_left:donut_right]
    left = middle.find(' ')
    if left == -1:
        continue
    left += donut_left
    inner_top = min(inner_top, i)
    inner_bottom = max(inner_bottom, i)
    inner_left = min(inner_left, left)
    right = middle.rfind(' ') + donut_left
    inner_right = max(inner_right, right)

print (donut_top, donut_left, donut_right, donut_bottom)
print (inner_top, inner_left, inner_right, inner_bottom)

## find portals
portals = {}

def scan(rmin, rmax, char_get, port_get, pos_get):
    global portals
    for i in range(rmin, rmax+1):
        c = char_get(i)
        if c < 'A' or c > 'Z':
            continue
        port = port_get(i, c)
        pos = pos_get(i)
        if port not in portals:
            portals[port] = []
        portals[port] += [pos]

# outer top border
scan(donut_left, donut_right,
    lambda i: lines[donut_top-1][i],
    lambda i, c: lines[donut_top-2][i] + c,
    lambda i: (i, donut_top))

# outer left border
scan(donut_top, donut_bottom,
    lambda i: lines[i][0],
    lambda i, c: c + lines[i][1],
    lambda i: (2, i))

# outer right border
scan(donut_top, donut_bottom,
    lambda i: lines[i][donut_right+1],
    lambda i, c: c + lines[i][donut_right+2],
    lambda i: (donut_right, i))

# outer bottom border
scan(donut_left, donut_right,
    lambda i: lines[donut_bottom+1][i],
    lambda i, c: c + lines[donut_bottom+2][i],
    lambda i: (i, donut_bottom))

# inner top border
scan(inner_left, inner_right,
    lambda i: lines[inner_top][i],
    lambda i, c: c + lines[inner_top+1][i],
    lambda i: (i, inner_top-1))

# inner left border
scan(inner_top, inner_bottom,
    lambda i: lines[i][inner_left],
    lambda i, c: c + lines[i][inner_left+1],
    lambda i: (inner_left-1, i))

# inner right border
scan(inner_top, inner_bottom,
    lambda i: lines[i][inner_right],
    lambda i, c: lines[i][inner_right-1] + c,
    lambda i: (inner_right+1, i))

# inner bottom border
scan(inner_left, inner_right,
    lambda i: lines[inner_bottom][i],
    lambda i, c: lines[inner_bottom-1][i] + c,
    lambda i: (i, inner_bottom+1))

for k, v in portals.items():
    print(k, v)

## Find paths through labyrinth
positions = {}
for port, poses in portals.items():
    for i, p in enumerate(poses):
        positions[p] = (port, i)

graph = {}
def in_donut(x, y):
    if y < donut_top or y > donut_bottom or x < donut_left or x > donut_right:
        return False
    if x >= inner_left and x <= inner_right and y >= inner_top and y <= inner_bottom:
        return False
    return True

def find_paths(port, index, pos):
    global graph
    global positions
    graph[(port, index)] = []
    q = [(pos, 0)]
    qpos = 0
    visited = set()
    while qpos < len(q):
        p, d = q[qpos]
        qpos += 1
        if p in visited:
            continue
        visited.add(p)
        if p != pos and p in positions:
            graph[(port, index)] += [(positions[p], d)]
            continue
        x, y = p
        for next in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
            nx, ny = next
            if lines[ny][nx] == '.' and next not in visited:
                q += [(next, d+1)]

for port, poses in portals.items():
    for i, p in enumerate(poses):
        find_paths(port, i, p)

for k, v in graph.items():
    print(k, v)

## Find shortest path from (AA, 0) to (ZZ, 0)
start = ('AA', 0)
finish = ('ZZ', 0)
s = set()
s.add(start[0])
q = [(0, start, s)]

while len(q):
    dist, node, vis = q[0]
    if node == finish:
        print('shortest path:', dist)
        break
    del q[0]
    vis.add(node[0])
    for next, adist in graph[node]:
        if next != finish:
            next = (next[0], -next[1] + 1)
            adist += 1
        if next[0] in vis:
            continue
        q += [(dist + adist, next, vis)]
    q.sort(key = lambda x: x[0])
    print(q)
