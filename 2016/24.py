#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import defaultdict, deque

e = Env(24)
e.T("""###########
#0.1.....2#
#.#######.#
#4.......3#
###########""", 14, None)


def find_numbers(g):
    count = 0
    start = None
    for row in range(g.h):
        for col in range(g.w):
            c = g.get(row, col)
            if c == '0':
                assert start is None
                start = (row, col)
            elif c > '0' and c <= '9':
                count += 1
    return start, count


def find_shortest_any_order(g, start, count):
    q = deque()
    targets = ""
    explored = defaultdict(list)
    q.append((start, 0, targets))
    while q:
        pos, dist, tgts = q.popleft()
        c = g.get(pos[0], pos[1])
        if c > '0' and c <= '9' and c not in tgts:
            # Add current position to targets
            tgts = ''.join(sorted([x for x in tgts] + [c]))
            if len(tgts) == count:
                # Reached all the numbers
                return dist
        if pos not in explored or tgts not in explored[pos]:
            explored[pos].append(tgts)
            for off in [(-1,0), (1,0), (0,-1), (0,1)]:
                nrow = pos[0] + off[0]
                ncol = pos[1] + off[1]
                if g.is_in(nrow, ncol) and g.get(nrow, ncol) != '#':
                    q.append(((nrow, ncol), dist + 1, tgts))
        # else: not a perspective path
    assert False, "path not found"


def part1(input):
    g = Grid(input.get_lines())
    start, count = find_numbers(g)
    return find_shortest_any_order(g, start, count)


e.run_tests(1, part1)
e.run_main(1, part1)


def find_shortest_with_return(g, start, count):
    q = deque()
    targets = ""
    explored = defaultdict(list)
    q.append((start, 0, targets))
    while q:
        pos, dist, tgts = q.popleft()
        c = g.get(pos[0], pos[1])
        if (c > '0' and c <= '9' and c not in tgts) \
            or (c == '0' and len(tgts) == count):
            # Add current position to targets
            tgts = ''.join(sorted([x for x in tgts] + [c]))
            if len(tgts) == count + 1:
                # Reached all the numbers and zero
                return dist
        if pos not in explored or tgts not in explored[pos]:
            explored[pos].append(tgts)
            for off in [(-1,0), (1,0), (0,-1), (0,1)]:
                nrow = pos[0] + off[0]
                ncol = pos[1] + off[1]
                if g.is_in(nrow, ncol) and g.get(nrow, ncol) != '#':
                    q.append(((nrow, ncol), dist + 1, tgts))
        # else: not a perspective path
    assert False, "path not found"


def part2(input):
    g = Grid(input.get_lines())
    start, count = find_numbers(g)
    return find_shortest_with_return(g, start, count)


# e.run_tests(2, part2)
e.run_main(2, part2)
