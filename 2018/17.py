#!/usr/bin/python3.8

from aoc import Env, Grid
import re
from collections import deque

SPRING = (500, 0)

e = Env(17)
e.T("""x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""", 57, None)

e.T("""x=495 y=2..7""", 6, None)

e.T("""x=500 y=2..7""", 12, None)
e.T("""x=500 y=4..9
x=495 y=2..4""", 16, None)

e.T("""x=492, y=2..10
x=508, y=2..10
y=10, x=492..508
x=495, y=4..7
x=503, y=4..7
y=4, x=495..503
y=7, x=495..503""", 0, None)


def get_lines(input):
    horizontal = []
    vertical = []
    hor_limit = [None, None]
    ver_limit = [None, None]

    limit_min = None
    limit_max = None

    def update_hor_limit(x):
        nonlocal hor_limit
        if hor_limit[0] is None or x < hor_limit[0]:
            hor_limit[0] = x
        if hor_limit[1] is None or x > hor_limit[1]:
            hor_limit[1] = x
    def update_ver_limit(y):
        nonlocal ver_limit
        if ver_limit[0] is None or y < ver_limit[0]:
            ver_limit[0] = y
        if ver_limit[1] is None or y > ver_limit[1]:
            ver_limit[1] = y

    update_hor_limit(SPRING[0])

    r = re.compile(r'\d+')
    for ln in input.get_valid_lines():
        nums = [int(x) for x in r.findall(ln)]
        assert len(nums) == 3, f"bad line {ln}"
        assert nums[1] < nums[2], f"failed assumption"
        if ln[0] == 'x':
            vertical.append(tuple(nums))
            update_hor_limit(nums[0])
            update_ver_limit(nums[1])
            update_ver_limit(nums[2])
        else:
            horizontal.append(tuple(nums))
            update_ver_limit(nums[0])
            update_hor_limit(nums[1])
            update_hor_limit(nums[2])

    horizontal.sort()
    vertical.sort()
    return horizontal, vertical, tuple(hor_limit), tuple(ver_limit)


def paint_ground_lines(grid, hor, ver):
    for y, minx, maxx in hor:
        assert y < grid.h, f"{y} < {grid.h}"
        for x in range(minx, maxx+1):
            assert x < grid.w, f"{x} < {grid.w}"
            grid.grid[y][x] = '#'

    for x, miny, maxy in ver:
        assert x < grid.w, f"{x} < {grid.w}"
        for y in range(miny, maxy+1):
            assert y < grid.h, f"{y} < {grid.h}"
            grid.grid[y][x] = '#'


def flood_ground(grid, spring, ver_limit):
    maxy = ver_limit[1]
    streams = deque()
    streams.append((spring, 'V'))
    # Some points will be visited multiple times, but we don't want
    # the number of combinations to explode, so keep track of points
    # that have already been explored.
    springs_used = set()
    # Lowest depth where the current basin has overflown.
    # Prevent multiple columns in a basin rising to different heights.
    # This would be necessary if water pressure applied, but it doesn't.
    #outflow = 0
    while streams:
        pos, ori = streams.popleft()
        if pos in springs_used:
            continue
        # print (pos, ori)
        springs_used.add(pos)
        x, y = pos
        if ori == 'V':
            # vertical flow
            y += 1
            while y <= maxy and grid.grid[y][x] == '.':
                grid.grid[y][x] = '~'
                y += 1
            if y <= maxy:
                streams.append(((x, y-1), 'H'))
        else:
            # horizontal flow
            assert y > 0
            #if y < outflow:
            #    continue
            grid.grid[y][x] = '~'
            # go left and right
            stops = []
            for d in [-1, 1]:
                _x = x + d
                while True:
                    assert x >= 0 and x < grid.w
                    if grid.grid[y][_x] == '#':
                        # clay barrier reached
                        stops += [_x - d]
                        break
                    grid.grid[y][_x] = '~'
                    if grid.grid[y+1][_x] == '.':
                        streams.append(((_x, y), 'V'))
                        #outflow = max(outflow, y)
                        break
                    _x += d
            # flow up if blocked on both ends
            if len(stops) == 2:
                # The water only rises along the vertical flow
                streams.append(((x, y-1), 'H'))
                # If water pressure would have applied, then this
                # would be the solution instead. But it doesn't.
                #for _x in range(stops[0], stops[1]+1):
                #    if grid.grid[y-1][_x] != '#':
                #        streams.append(((_x, y-1), 'H'))

    grid.grid[spring[1]][spring[0]] = '+'


def print_ground(grid, hor_limit, ver_limit):
    xrange = (max(0, hor_limit[0]-1), hor_limit[1]+2)
    yrange = (0, ver_limit[1]+1)
    print(f"x from {xrange[0]} to {xrange[1]}")
    print(f"y from {yrange[0]} to {yrange[1]}")
    for y in range(yrange[0], yrange[1]):
        line = ''.join([grid.grid[y][x] for x in range(xrange[0], xrange[1])])
        print(line)


def count_wet(grid, hor_limit, ver_limit):
    xrange = (max(0, hor_limit[0]-1), hor_limit[1]+2)
    yrange = (ver_limit[0], ver_limit[1]+1)
    counter = 0
    for y in range(yrange[0], yrange[1]):
        counter += sum([1 for x in range(xrange[0], xrange[1]) if grid.grid[y][x] == '~'])
    return counter


def part1(input):
    hor, ver, hor_limit, ver_limit = get_lines(input)
    width = hor_limit[1] + 2
    height = ver_limit[1] + 1
    #print(width, height)
    grid = Grid(['.' * width for _ in range(height)])
    paint_ground_lines(grid, hor, ver)
    flood_ground(grid, SPRING, ver_limit)
    print_ground(grid, hor_limit, ver_limit)
    return count_wet(grid, hor_limit, ver_limit)


e.run_tests(1, part1)
#e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
