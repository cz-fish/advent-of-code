#!/usr/bin/python3.8

from aoc import Env

e = Env(9)
e.T("""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""", 13, 1)

e.T("""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""", None, 36)


def make_instr(lines):
    instr = []
    for ln in lines:
        parts = ln.split(' ')
        assert len(parts) == 2
        instr.append((parts[0], int(parts[1])))
    return instr


def snap_tail(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        # they overlap, or are adjacent
        return tail
    if dx == 0:
        # same column
        if dy > 0:
            return (tail[0], tail[1] + 1)
        else:
            return (tail[0], tail[1] - 1)
    elif dy == 0:
        # same row
        if dx > 0:
            return (tail[0] + 1, tail[1])
        else:
            return (tail[0] - 1, tail[1])
    else:
        if abs(dx) > abs(dy):
            if dx > 0:
                return (head[0] - 1, head[1])
            else:
                return (head[0] + 1, head[1])
        elif abs(dx) < abs(dy):
            if dy > 0:
                return (head[0], head[1] - 1)
            else:
                return (head[0], head[1] + 1)
        else:
            # In part 1, this doesn't happen.
            # In part 2, the head can move diagonally away from tail
            dx = dx // abs(dx)
            dy = dy // abs(dy)
            return (tail[0] + dx, tail[1] + dy)


def trace_tail(instr):
    points = set()
    head = (0, 0)
    tail = (0, 0)
    points.add(tail)
    directions = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
    for d, a in instr:
        move = directions[d]
        for step in range(a):
            head = (head[0] + move[0], head[1] + move[1])
            tail = snap_tail(head, tail)
            points.add(tail)
    return points


def part1(input):
    instr = make_instr(input.get_valid_lines())
    points = trace_tail(instr)
    return len(points)


e.run_tests(1, part1)
e.run_main(1, part1)

def print_points(points):
    pts = list(points)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mx = min(xs)
    Mx = max(xs)
    my = min(ys)
    My = max(ys)
    grid = [['.' for _ in range(mx, Mx + 1)] for _ in range(my, My + 1)]
    for p in pts:
        grid[p[1]-my][p[0]-mx] = '#'
    for ln in grid:
        print(''.join(ln))


def trace_tail_multi(instr, num_knots):
    points = set()
    knots = [(0, 0) for _ in range(num_knots)]
    points.add(knots[-1])
    directions = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}
    for d, a in instr:
        move = directions[d]
        for step in range(a):
            for k in range(num_knots):
                knot = knots[k]
                if k == 0:
                    knot = (knot[0] + move[0], knot[1] + move[1])
                else:
                    knot = snap_tail(knots[k-1], knot)
                knots[k] = knot
            points.add(knots[-1])
    return points

def part2(input):
    instr = make_instr(input.get_valid_lines())
    points = trace_tail_multi(instr, 10)
    print_points(points)
    return len(points)


e.run_tests(2, part2)
e.run_main(2, part2)
