#!/usr/bin/python3.8

from pyaoc import Env, Grid
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
y=13, x=498..504""", 57, 14+15)

e.T("""x=495 y=2..7""", 6, 0)

e.T("""x=500 y=2..7""", 12, 0)

e.T("""x=500 y=4..9
x=495 y=2..4""", 16, 0)

e.T("""x=492, y=2..10
x=508, y=2..10
y=10, x=492..508
x=495, y=4..7
x=503, y=4..7
y=4, x=495..503
y=7, x=495..503""", 102, 15*4+6*4)

e.T("""x=499 y=2..3
x=501 y=2..3
y=3 x=499..501
x=500 y=5..6
x=502 y=5..6
y=6 x=500..502
x=495 y=8..10
x=505 y=8..10
y=10 x=495..505
x=510 y=2..10""", 55, 1+1+9*2)

e.T("""x=497 y=2..3
x=503 y=2..3
y=3 x=497..503
x=492 y=6..12
x=508 y=7..12
y=12 x=492..508
x=498 y=5..8
x=502 y=6..8
y=8 x=498..502""", 109, 5+5*5+15*3)


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


def print_ground(grid, hor_limit, ver_limit):
    xrange = (max(0, hor_limit[0]-1), hor_limit[1]+2)
    yrange = (0, ver_limit[1]+1)
    #print(f"x from {xrange[0]} to {xrange[1]}")
    #print(f"y from {yrange[0]} to {yrange[1]}")
    for y in range(yrange[0], yrange[1]):
        line = ''.join([grid.grid[y][x] for x in range(xrange[0], xrange[1])])
        print(line)


def find_line_boundary(grid, x, y, delta):
    while grid.grid[y][x] in '.|':
        if grid.grid[y+1][x] in '.|':
            return x, False
        x += delta
    return x - delta, True


def fill_pot(grid, x, y):
    # Make horizontal lines of water blocks from the starting position x, y
    # left and right until the nearest obstacle in each direction. If neither
    # side or just one side is blocked, then this is a top wet line. If both
    # sides are blocked then the line belongs to a basin, and the water flows
    # one more level up. Repeat this process until the top level line is found.
    # Each pot should have either one or two overflows (the end of the top line
    # that is not obstructed), and the coordinates of these are returned.
    overflows = []
    while not overflows:
        assert y > 0, f"overflowing too high up when filling up pot at x={x}"
        lbound, lblocked = find_line_boundary(grid, x-1, y, -1)
        rbound, rblocked = find_line_boundary(grid, x+1, y, 1)
        if not lblocked:
            overflows.append((lbound, y))
        if not rblocked:
            overflows.append((rbound, y))
        char = '~' if not overflows else '|'
        for _x in range(lbound, rbound+1):
            grid.grid[y][_x] = char
        y -= 1
    return overflows


def flood_ground(grid, spring, ver_limit):
    maxy = ver_limit[1]
    streams = deque()
    streams.append((spring, 'V'))

    while streams:
        pos, ori = streams.popleft()
        # print (pos, ori)
        x, y = pos
        if ori == 'V':
            # vertical flow
            y += 1
            while y <= maxy and grid.grid[y][x] == '.':
                grid.grid[y][x] = '|'
                y += 1
            # We've found the edge of the map, or an obstacle
            # If it's an obstacle, and it isn't another vertical
            # stream already, then add a horizontal stream at that point
            if y <= maxy and grid.grid[y][x] != '|':
                streams.append(((x, y-1), 'H'))
        else:
            # horizontal flow
            assert y > 0
            overflows = fill_pot(grid, x, y)
            for overflow in overflows:
                streams.append((overflow, 'V'))

    grid.grid[spring[1]][spring[0]] = '+'


def count_wet(grid, hor_limit, ver_limit, dry_only=False):
    significant = '~' if dry_only else '~|'
    xrange = (max(0, hor_limit[0]-1), hor_limit[1]+2)
    yrange = (ver_limit[0], ver_limit[1]+1)
    counter = 0
    for y in range(yrange[0], yrange[1]):
        counter += sum([1 for x in range(xrange[0], xrange[1]) if grid.grid[y][x] in significant])
    return counter


def sanity_check_solution(grid, ver_limit):
    # Check that there is at least one overflow at the very bottom of the grid
    for x in range(0, grid.w):
        if grid.grid[ver_limit[1]][x] == '|':
            #print(f'wet at {x}, {ver_limit[1]}')
            return True
    else:
        assert False, f"Water didn't overflow to level {ver_limit[1]}"


def common_part(input):
    hor, ver, hor_limit, ver_limit = get_lines(input)
    width = hor_limit[1] + 2
    height = ver_limit[1] + 1
    grid = Grid(['.' * width for _ in range(height)])
    paint_ground_lines(grid, hor, ver)
    flood_ground(grid, SPRING, ver_limit)
    # uncomment to see the magic
    #print_ground(grid, hor_limit, ver_limit)
    sanity_check_solution(grid, ver_limit)
    return grid, hor_limit, ver_limit


def part1(input):
    grid, hor_limit, ver_limit = common_part(input)
    return count_wet(grid, hor_limit, ver_limit)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    grid, hor_limit, ver_limit = common_part(input)
    return count_wet(grid, hor_limit, ver_limit, dry_only=True)


e.run_tests(2, part2)
e.run_main(2, part2)
