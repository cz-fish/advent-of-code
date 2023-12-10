#!/usr/bin/python3.8

from aoc import Env, Grid

def eT(*a):
    pass

e = Env(10)
e.T(""".....
.S-7.
.|.|.
.L-J.
.....""", 4, 1)
e.T("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...""", 8, 1)
e.T("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""", None, 4)
e.T(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""", None, 8)
e.T("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""", None, 10)


def find_start(grid):
    for row, ln in enumerate(grid.grid):
        if 'S' in ln:
            return row, ln.index('S')
    assert False, "Cannot find start S"

def trace_from_start(grid, start, go_dir):
    offsets = {
        0: (-1, 0),
        1: (0, 1),
        2: (1, 0),
        3: (0, -1),
    }
    dirs = {
        '|': [0, 2],
        '-': [1, 3],
        'L': [0, 1],
        'J': [0, 3],
        '7': [2, 3],
        'F': [1, 2],
    }
    steps = 1
    corner_points = []
    all_points = set()
    row = start[0] + offsets[go_dir][0]
    col = start[1] + offsets[go_dir][1]
    corner_points.append(start)
    all_points.add(start)
    while (row, col) != start:
        if not grid.is_in(row, col):
            # out of bounds
            return -1, None, None
        pipe = grid.get(row, col)
        if pipe not in dirs:
            # landed on a '.'
            return -1, None, None
        if pipe in "LJ7F":
            corner_points.append((row, col))
        all_points.add((row, col))
        # Each pipe segment has two directions. We've arrived from one of those
        # directions, so we must continue vie the other direction.
        # Previous tile's up is the current tile's down, so rotate the go_dir by 2
        # (the order of `dirs` is up, right, down, left, so opposites are always with offset of 2)
        go_dir = (go_dir + 2) % 4
        if go_dir == dirs[pipe][0]:
            # We came from direction [0], so we will continue in direction [1]
            go_dir = dirs[pipe][1]
        elif go_dir == dirs[pipe][1]:
            # We came from direction [1], so we will continue in direction [0]
            go_dir = dirs[pipe][0]
        else:
            # We came from a direction that is invalid for the current segment. That is an error
            return -1, None, None
        row += offsets[go_dir][0]
        col += offsets[go_dir][1]
        steps += 1
    return steps, corner_points, all_points


def part1(input):
    grid = Grid(input.get_valid_lines())
    start = find_start(grid)
    lengths = set([
        dist for dist, _, _ in [
            trace_from_start(grid, start, d) for d in range(4)
        ] if dist != -1
    ])
    assert len(lengths) == 1
    length = list(lengths)[0]
    assert length % 2 == 0
    return length // 2


e.run_tests(1, part1)
e.run_main(1, part1)


def split_path_to_segments(points):
    hor = []
    ver = []
    for i, A in enumerate(points):
        B = points[(i + 1) % len(points)]
        if A[0] == B[0]:
            assert A[1] != B[1]
            # same row, horizontal line
            hor.append((A[0], min(A[1], B[1]), max(A[1], B[1])))
        elif A[1] == B[1]:
            assert A[0] != B[0]
            # same column, vertical line
            ver.append((A[1], min(A[0], B[0]), max(A[0], B[0])))
        else:
            assert False, "path segment neither fully horizontal nor fully verical"
    return hor, ver


def point_is_in(row, col, hor, ver):
    left = 0
    for c, m, M in ver:
        if c < col and m <= row and M > row:
            left += 1
    if left % 2 == 1:
        return True
    above = 0
    for r, m, M in hor:
        if r < row and m <= col and M > col:
            above += 1
    if above %2 == 1:
        return True
    return False


def count_inside(grid, start):
    for go_dir in range(4):
        _, corner_points, all_points = trace_from_start(grid, start, go_dir)
        if corner_points is not None:
            break
    else:
        assert False, "cannot find any vertical points"

    hor, ver = split_path_to_segments(corner_points)

    points_in = 0
    for row in range(grid.h):
        for col in range(grid.w):
            if (row, col) not in all_points \
              and point_is_in(row, col, hor, ver):
                points_in += 1
                #print(f"point is in: {row}, {col}")
    return points_in

def part2(input):
    grid = Grid(input.get_valid_lines())
    start = find_start(grid)
    return count_inside(grid, start)


e.run_tests(2, part2)
e.run_main(2, part2)
