#!/usr/bin/python3.8

from pyaoc import Env
from collections import deque

e = Env(18)
e.T("""1,1,1
2,1,1""", 10, 10)
e.T("""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""", 64, 58)


SIX_DIRECTIONS = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, -1], [0, -1, 0], [-1, 0, 0]]


def make_point_cloud(input):
    minCoords = None
    maxCoords = None
    cloud = set()
    for ln in input.get_valid_lines():
        coords = [int(x) for x in ln.split(',')]
        assert len(coords) == 3
        if minCoords is None:
            minCoords = coords[:]
        if maxCoords is None:
            maxCoords = coords[:]
        # keep track of min/max limits of all coords
        for d in range(3):
            if coords[d] < minCoords[d]:
                minCoords[d] = coords[d]
            if coords[d] > maxCoords[d]:
                maxCoords[d] = coords[d]
        ctuple = tuple(coords)
        assert ctuple not in cloud, f"There is a duplicate point {coords}"
        cloud.add(ctuple)

    if min(minCoords) < 0:
        # there's no reason why the coords couldn't be negative ... just curious
        print(f"Note: There are negative values... {minCoords} .. {maxCoords}")

    return cloud, minCoords, maxCoords


def cound_sides(cloud):
    counter = 0
    for pt in cloud:
        for adj in SIX_DIRECTIONS:
            nei = (pt[0] + adj[0], pt[1] + adj[1], pt[2] + adj[2])
            if nei not in cloud:
                counter += 1
    return counter


def part1(input):
    cloud, _, _ = make_point_cloud(input)
    return cound_sides(cloud)


e.run_tests(1, part1)
e.run_main(1, part1)

def count_outer_sides(cloud, mins, maxs):
    count = 0
    # Flood fill from 1 outside the min/max coords
    visited = set()
    q = deque()
    start = (mins[0]-1, mins[1]-1, mins[2]-1)
    q.append(start)
    visited.add(start)
    while q:
        p = q.popleft()
        for step in SIX_DIRECTIONS:
            a = (p[0] + step[0], p[1] + step[1], p[2] + step[2])
            if a[0] < mins[0]-1 or a[1] < mins[1]-1 or a[2] < mins[2]-1 \
                or a[0] > maxs[0]+1 or a[1] > maxs[1]+1 or a[2] > maxs[2]+1:
                continue
            if a in visited:
                continue
            if a in cloud:
                count += 1
            else:
                q.append(a)
                visited.add(a)
    return count


def part2(input):
    cloud, mins, maxs = make_point_cloud(input)
    return count_outer_sides(cloud, mins, maxs)


e.run_tests(2, part2)
e.run_main(2, part2)
