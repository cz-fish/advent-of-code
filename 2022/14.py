#!/usr/bin/python3.8

from aoc import Env

e = Env(14)
e.T("""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""", 24, 93)


SOURCE = (500, 0)


def get_lines(inp_lines):
    lines = []
    for ln in inp_lines:
        lines.append([[int(x) for x in pt.split(',')] for pt in ln.split(' -> ')])
    return lines


def find_min_max(lines):
    min_x = None
    max_x = None
    min_y = 0
    max_y = None
    for line in lines:
        for pt in line:
            if min_x is None or pt[0] < min_x:
                min_x = pt[0]
            if max_x is None or pt[0] > max_x:
                max_x = pt[0]
            if pt[1] < min_y:
                assert False, "negative Y coord"
            if max_y is None or pt[1] > max_y:
                max_y = pt[1]
    assert min_x is not None and max_x is not None and max_y is not None
    # add one on each side
    min_x -= 1
    max_x += 1
    return min_x, min_y, max_x - min_x + 1, max_y - min_y + 1


def draw_line(scan, offset, pt1, pt2):
    dx = pt2[0] - pt1[0]
    dy = pt2[1] - pt1[1]
    assert dx == 0 or dy == 0, f"Line not horizontal or vertical: {pt1} {pt2}"
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    pt = pt1
    while pt != pt2:
        scan[pt[1] - offset[1]][pt[0] - offset[0]] = '#'
        pt[0] += dx
        pt[1] += dy
    scan[pt2[1] - offset[1]][pt2[0] - offset[0]] = '#'


def make_scan(offset, width, height, lines):
    scan = [[
        '.' for _ in range(offset[0], offset[0] + width)
    ] for _ in range(offset[1], offset[1] + height)]

    for line in lines:
        assert len(line) > 1, f"Line with less than 2 points {line}"
        for pt_index in range(1, len(line)):
            draw_line(scan, offset, line[pt_index - 1], line[pt_index])

    return scan


def print_scan(scan, offset):
    for y, ln in enumerate(scan):
        if y == 0:
            d = SOURCE[0] - offset[0]
            print(''.join(ln[:d]) + '+' + ''.join(ln[d+1:]))
        else:
            print(''.join(ln))
    print('\n-------------------\n')


def sand_flood(scan, offset, max_y):
    counter = 0
    # down, left-down, right-down in this order
    fall_directions = [[0, 1], [-1, 1], [1, 1]]
    while True:
        grain = [SOURCE[0], SOURCE[1]]
        if scan[grain[1] - offset[1]][grain[0] - offset[0]] != '.':
            # source blocked
            return counter
        while True:
            if grain[1] >= max_y:
                # grain falls off. Stop
                return counter
            for direction in fall_directions:
                nx = grain[0] + direction[0]
                ny = grain[1] + direction[1]
                if scan[ny - offset[1]][nx - offset[0]] == '.':
                    grain = [nx, ny]
                    break
            else:
                # nowhere to fall, settle
                scan[grain[1] - offset[1]][grain[0] - offset[0]] = 'o'
                counter += 1
                break
        # next grain
    # unreachable


def part1(input):
    lines = get_lines(input.get_valid_lines())
    min_x, min_y, width, height = find_min_max(lines)
    offset = (min_x, min_y)
    scan = make_scan(offset, width, height, lines)
    # print_scan(scan, offset)
    val = sand_flood(scan, offset, height-1)
    # print_scan(scan, offset)
    return val


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = get_lines(input.get_valid_lines())
    min_x, min_y, width, height = find_min_max(lines)
    min_x = min(min_x + 1, SOURCE[0] - height) - 1
    max_x = max(min_x + width - 1, SOURCE[0] + height) + 1
    offset = (min_x, min_y)
    width = max_x - min_x + 1
    height += 2
    scan = make_scan(offset, width, height, lines)
    # add bottom line
    for x in range(width):
        scan[height-1][x] = '#'
    # print_scan(scan, offset)
    val = sand_flood(scan, offset, height-1)
    # print_scan(scan, offset)
    return val


e.run_tests(2, part2)
e.run_main(2, part2)
