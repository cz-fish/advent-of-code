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
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            if c not in distances:
                # found shortest distance to a new key
                distances[c] = dist
        visited.add((x, y))
        for next in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            if next in visited:
                continue
            q += [(next[0], next[1], dist+1)]
    return distances

doors = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
keys = 'abcdefghijklmnopqrstuvwxyz'
unlocked = set(doors)
all_dists = {}
for k in pos.keys():
    all_dists[k] = paths_from(k, unlocked)

def build_tree(root_symbol):
    p = pos[root_symbol]
    tree = {root_symbol: ['', '']}
    q = [(p[0], p[1], 0, root_symbol)]
    qpos = 0
    visited = set()
    while qpos < len(q):
        x, y, dist, path = q[qpos]
        qpos += 1
        c = grid[y][x]
        if c == '#' or (x, y) in visited:
            continue
        if (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
            prev = path[-1]
            tree[prev][0] += c
            tree[c] = ['', prev]
            path += c
        visited.add((x, y))
        for next in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            if next in visited:
                continue
            q += [(next[0], next[1], dist+1, path)]
    return tree

def print_node(tree, node, leaders):
    root = tree[node][0]
    for i, c in enumerate(root):
        if i > 0:
            print(leaders + '\\', end='')
        else:
            print('+', end= '')
        print(f'-{c}', end = '')
        if tree[c][0]:
            print('-', end = '')
            if i == len(root) - 1:
                nleaders = leaders + '    '
            else:
                nleaders = leaders + '|   '
            print_node(tree, c, nleaders)
        else:
            print('')


def print_tree(tree):
    print_node(tree, '@', '')

def remove_from_tree(tree, removals):
    for n in tree.keys():
        children = ''.join([c for c in tree[n][0] if c not in removals])
        if n in removals:
            k = n
            while k in removals:
                k = tree[k][1]
            for c in children:
                tree[c][1] = k
            tree[k][0] += children
        else:
            tree[n][0] = children

    for r in removals:
        if r in tree:
            del tree[r]


def prune_tree(tree):
    # remove branches that are only doors
    change = True
    removed = set()
    while change:
        change = False
        for c in doors:
            if c not in tree:
                continue
            t = ''.join([r for r in tree[c][0] if r in tree and (tree[r][0] or r in keys)])
            if t != tree[c][0]:
                change = True
            if not t:
                del tree[c]
                removed.add(c)
            else:
                tree[c][0] = t
    remove_from_tree(tree, removed)

    # remove doors that are preceded by their key on the same branch
    q = [('@', '')]
    qpos = 0
    useless_doors = set()
    while qpos < len(q):
        node, path = q[qpos]
        qpos += 1
        if node in doors:
            key = node.lower()
            if key in path:
                useless_doors.add(node)
        for c in tree[node][0]:
            q += [(c, path + node)]
    remove_from_tree(tree, useless_doors)

    remaining_doors = set()
    for door in doors:
        if door in tree:
            remaining_doors.add(door)

    # find useful keys (at leaf nodes, or opening remaining doors)
    useful_keys = set()
    for key in keys:
        if key not in tree:
            continue
        if not tree[key][0] or key.upper() in remaining_doors:
            # leaf or key with a door
            useful_keys.add(key)

    useless_keys = set(keys) - useful_keys
    remove_from_tree(tree, useless_keys)
    return useful_keys

def shortest_path(tree, start, num_keys):
    q = [(0, start, '', '', start)]
    loops = 0
    while q:
        loops += 1
        #if loops == 10:
        #    return 0
        if loops % 1000 == 0:
            print('loops', loops, 'queue', len(q))
        dist, node, mykeys, options, path = q[0]
        #print(q[0])
        q = q[1:]
        if len(mykeys) == num_keys:
            print(dist, path)
            return dist
        options += tree[node][0]
        for o in options:
            if o in doors:
                key = o.lower()
                if key not in mykeys:
                    # door is locked
                    continue
            add_dist = all_dists[node][o]
            newkeys = mykeys[:]
            if o in keys:
                newkeys += o
            newoptions = options.replace(o, '')
            q += [(dist + add_dist, o, newkeys, newoptions, path + o)]
        q.sort(key=lambda n: n[0])
    raise "Path not found"


tree = build_tree('@')
print_tree(tree)
remaining_keys = prune_tree(tree)
print("------")
print("pruned")
print("------")
print_tree(tree)
print(f'remaining keys: {len(remaining_keys)}')
dist = shortest_path(tree, '@', len(remaining_keys))

"""
path = '@vtkbeafohygwz'

total = 0
for i in range(1, len(path)):
    f = path[i-1]
    t = path[i]
    di = all_dists[f][t]
    print(f'from {f} to {t} dist {di}')
    total += di
print(f'total {total}')
"""
