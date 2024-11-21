#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict, deque


e = Env(22)
e.T("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""", 5, 7)


def parse_bricks(lines):
    bricks = []
    for ln in lines:
        tl, br = ln.split('~')
        a,b,c = [int(x) for x in tl.split(',')]
        d,e,f = [int(x) for x in br.split(',')]
        bricks.append((min(a, d), min(b, e), min(c, f), max(a, d), max(b, e), max(c, f)))
    return bricks


def drop_bricks(falling):
    heightmap = {}
    dropped = []
    supports = {}
    for index, brick in enumerate(falling):
        left, front, bottom, right, back, top = brick
        min_level = 0
        supporters = set()
        for x in range(left, right + 1):
            for y in range(front, back + 1):
                level = 0
                if (x, y) in heightmap:
                    level, supporter = heightmap[(x, y)]
                    if level > min_level:
                        supporters = set()
                    if level >= min_level:
                        supporters.add(supporter)
                min_level = max(min_level, level)
        assert min_level < bottom, f"Brick {brick} below heightmap level {min_level}"
        drop = bottom - min_level - 1
        dropped.append((left, front, bottom - drop, right, back, top - drop))
        supports[index] = supporters
        # update heightmap
        for x in range(left, right + 1):
            for y in range(front, back + 1):
                heightmap[(x, y)] = (top - drop, index)
    return dropped, supports


def count_voxels(bricks):
    voxels = 0
    for brick in bricks:
        a, b, c, d, e, f = brick
        voxels += ((d-a+1) * (e-b+1) * (f-c+1))
    print(voxels)


def part1(input):
    bricks = parse_bricks(input.get_valid_lines())
    # sort the bricks by bottom coordinate ascending
    bricks.sort(key=lambda brick: brick[2])
    dropped, supports = drop_bricks(bricks)

    non_removable = set()
    for brick, sup in supports.items():
        if len(sup) == 1:
            non_removable.add(list(sup)[0])
    return len(bricks) - len(non_removable)


e.run_tests(1, part1)
e.run_main(1, part1)


def count_chain_drops(n_bricks, is_supported_by, supports):
    # just try removing every brick with cascade
    total = 0
    for i in range(n_bricks):
        removed = set()
        unblockers = defaultdict(set)
        unblockers[i] = set(supports[i])
        q = deque([i])
        while q:
            brick = q.popleft()
            removed.add(brick)
            for unblocked in unblockers[brick]:
                still_supported = False
                for support in is_supported_by[unblocked]:
                    if support not in removed:
                        still_supported = True
                        unblockers[support].add(unblocked)
                if not still_supported:
                    q.append(unblocked)
                    unblockers[unblocked] = set(supports[unblocked])
        total += len(removed) - 1
    return total


def part2(input):
    bricks = parse_bricks(input.get_valid_lines())
    # sort the bricks by bottom coordinate ascending
    bricks.sort(key=lambda brick: brick[2])
    dropped, supports = drop_bricks(bricks)

    pillars = {
        i: set() for i in range(len(bricks))
    }
    for above, below in supports.items():
        for brick in below:
            pillars[brick].add(above)

    # supports: for each brick (key), set of all bricks supporting it (value)
    # pillars: for each brick (key), set of all bricks supported by it (value)
    return count_chain_drops(len(bricks), supports, pillars)


e.run_tests(2, part2)
e.run_main(2, part2)
