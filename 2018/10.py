#!/usr/bin/python3.8

from aoc import Env
import re

e = Env(10, [], {
    'maxcluster': 30,
    'maxstep': 1000,
    'skip': 10000    # the coords are large, we fast-forward 10k steps at the beginning
})
e.T("""position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""", True, None, {
    'maxcluster': 10,
    'maxstep': 10,
    'skip': 0
})


def extremes(points):
    left = min([p[0] for p in points])
    right = max([p[0] for p in points])
    top = min([p[1] for p in points])
    bottom = max([p[1] for p in points])
    return left, right, top, bottom


def next_step(points, step=1):
    for pt in points:
        pt[0] += pt[2] * step
        pt[1] += pt[3] * step


def detect_clusters(points):
    """Return true if the points seem to be aligned to show a message,
       false otherwise. To be considered aligned, all the points must
       be within a 300x300 square (this constraint could be smaller),
       and they must form fewer than param['maxcluster'] connected
       clusters - which is a simple detection that the points form
       some sort of letters."""
    left, right, top, bottom = extremes(points)
    w = right - left + 1
    h = bottom - top + 1
    if w > 300 or h > 300:
        return False

    # This is basically counting clouds. Turn the grid into a set
    # (called soup) for easier detection of clusters
    soup = set()
    for pt in points:
        soup.add((pt[0], pt[1]))

    def remove_cluster(point):
        if point not in soup:
            return 0
        soup.remove(point)
        return 1 + \
            remove_cluster((point[0]-1, point[1])) + \
            remove_cluster((point[0]+1, point[1])) + \
            remove_cluster((point[0], point[1]-1)) + \
            remove_cluster((point[0], point[1]+1)) + \
            remove_cluster((point[0]-1, point[1]-1)) + \
            remove_cluster((point[0]-1, point[1]+1)) + \
            remove_cluster((point[0]+1, point[1]-1)) + \
            remove_cluster((point[0]+1, point[1]+1))

    clusters = []
    while soup:
        point = soup.pop()
        soup.add(point)
        size = 1 + remove_cluster(point)
        clusters += [size]

    return len(clusters) < e.get_param()['maxcluster']


def print_points(points):
    left, right, top, bottom = extremes(points)
    w = right - left + 1
    h = bottom - top + 1
    grid = [['.' for _ in range(w)] for _ in range(h)]
    for pt in points:
        grid[pt[1] - top][pt[0] - left] = '#'
    for ln in grid:
        print(''.join(ln))


def part1(input):
    points = []
    for ln in input.get_valid_lines():
        vals = re.findall(r'-?\d+', ln)
        points += [[int(x) for x in vals]]
    counter = 0
    skip = e.get_param()['skip']
    if skip:
        next_step(points, skip)
    while True:
        counter += 1
        next_step(points)
        if detect_clusters(points):
            break
        if counter > e.get_param()['maxstep']:
            return False
    print_points(points)
    counter += skip
    print(f"After {counter} steps (=part2)")
    return True


e.run_tests(1, part1)
e.run_main(1, part1)
