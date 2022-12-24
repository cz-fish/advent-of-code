#!/usr/bin/python3.8

from aoc import Env, Grid, Integers
from collections import deque

e = Env(24)
e.T("""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""", 18, 54)


def capture_blizzards(input):
    grid = Grid(input.get_valid_lines())
    horizontals = [
        ['.' for _ in range(grid.w - 2)]
        for _ in range(grid.h - 2)
    ]
    verticals = [
        ['.' for _ in range(grid.h - 2)]
        for _ in range(grid.w - 2)
    ]
    for y in range(1, grid.h - 1):
        for x in range(1, grid.w - 1):
            c = grid.get(y, x)
            if c in '<>':
                horizontals[y-1][x-1] = c
            elif c in 'v^':
                verticals[x-1][y-1] = c
    return horizontals, verticals


def find_free_points(line, coord, is_x, free_set):
    move = set()
    for i, c in enumerate(line):
        if c in '<^':
            move.add((i, -1))
        elif c in '>v':
            move.add((i, 1))
    ll = len(line)
    for time in range(ll):
        occupied = set()
        for p, d in move:
            occupied.add((p + d * time) % ll)
        for x in range(ll):
            if x not in occupied:
                if is_x:
                    free_set.add((time, coord, x))
                else:
                    free_set.add((time, x, coord))


def find_shortest_time(start, end, free, period, time_offset):
    q = deque()
    q.append((0, start[0], start[1]))
    reached = set()
    reached.add((time_offset, start[0], start[1]))
    d = [(1, 0), (0, 1), (0, -1), (-1, 0), (0, 0)]
    iter = 0
    while q:
        time, x, y = q.popleft()
        iter += 1
        if (x, y) == end:
            return time
        
        for dx, dy in d:
            ntime = time + 1
            nmtime = (ntime + time_offset) % period
            nx = x + dx
            ny = y + dy
            p = (nmtime, nx, ny)
            if p in free and p not in reached:
                q.append((ntime, nx, ny))
                reached.add(p)
    assert False, f"solution not found after {iter} steps. reached = {len(reached)}"


def set_up_search_space(input):
    # split input to horizontally moving blizzards and vertically moving blizzards
    hor, ver = capture_blizzards(input)

    #print("horizontals")
    #for ln in hor:
    #    print(''.join(ln))
    #print("verticals")
    #for y in range(len(ver[0])):
    #    print(''.join([ver[x][y] for x in range(len(ver))]))

    height = len(hor)
    width = len(ver)

    # Find horizontally free spots, and vertically free spots
    # in 3d space (time, x, y).
    hor_free = set()
    for y in range(len(hor)):
        find_free_points(hor[y], y, False, hor_free)
    ver_free = set()
    for x in range(len(ver)):
        find_free_points(ver[x], x, True, ver_free)

    # Then intersect the two groups to find globally free spots.
    # Do this for time from 0 to lowest-common-multiple
    # of width and height (the overall repetition period)
    period = Integers.lcm(height, width)

    free = set() # (time, x, y)
    for time in range(period):
        for x in range(width):
            for y in range(height):
                if (time % width, x, y) in hor_free and (time % height, x, y) in ver_free:
                    free.add((time, x, y))
        # make the origin and destination free at any time
        free.add((time, 0, -1))
        free.add((time, width-1, height))

    return free, width, height, period


def part1(input):
    free, width, height, period = set_up_search_space(input)

    return find_shortest_time((0, -1), (width-1, height), free, period, 0)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    free, width, height, period = set_up_search_space(input)

    there = find_shortest_time((0, -1), (width-1, height), free, period, 0)
    print(f"there in {there} steps")
    back = find_shortest_time((width-1, height), (0, -1), free, period, there)
    print(f"back in another {back} steps")
    there_again = find_shortest_time((0, -1), (width-1, height), free, period, there + back)
    print(f"there again in another {there_again} steps")
    return there + back + there_again


e.run_tests(2, part2)
e.run_main(2, part2)
