#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict

def eT(*a):
    pass

e = Env(18)
e.T("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""", 62, 952408144115)

#  ######
#  #    #
#  ###  #
#    #  #
#    ####
# 6 + 6 + 6 + 4 + 4 = 26
e.T("""U 2 ()
L 2 ()
U 2 ()
R 5 ()
D 4 ()
L 3 ()""", 26, None)

#  #######
#  #     #
#  # ### #
#  # # # #
#  ### ###
# 7 + 7 + 7 + 6 + 6 = 33
e.T("""R 6 ()
D 4 ()
L 2 ()
U 2 ()
L 2 ()
D 2 ()
L 2 ()
U 4 ()""", 33, None)

def parse_line_segments(lines):
    row = 0
    col = 0
    m_row = 0
    M_row = 0
    m_col = 0
    M_col = 0
    segments = []
    for ln in lines:
        d, l, c = ln.split()
        assert c.startswith('(') and c.endswith(')')
        length = int(l)
        segments.append(((row, col), d, length, c[1:-1]))
        if d == 'R':
            col += length
        elif d == 'D':
            row += length
        elif d == 'L':
            col -= length
        elif d == 'U':
            row -= length
        else:
            assert False, f"Wrong direction {d}"
        m_row = min(m_row, row)
        m_col = min(m_col, col)
        M_row = max(M_row, row)
        M_col = max(M_col, col)
    return segments, (m_row, M_row, m_col, M_col)


def draw(segments, limits):
    m_row, M_row, m_col, M_col = limits
    width = M_col - m_col + 1
    height = M_row - m_row + 1
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for start, d, length, _ in segments:
        row, col = start
        for i in range(length):
            r = row
            c = col
            if d == 'R':
                c += i
            elif d == 'D':
                r += i
            elif d == 'L':
                c -= i
            elif d == 'U':
                r -= i
            assert r - m_row < height, f"{start} r {r} {m_row} {height}"
            assert c - m_col < width, f"{start} c {c} {m_col} {width}"
            grid[r - m_row][c - m_col] = '#'
    with open('18.xpm', 'wt') as f:
        print('! XPM2', file=f)
        print(f'{M_col - m_col + 1} {M_row - m_row + 1} 2 1', file=f)
        print('# c #ff0000', file=f)
        print('. c #444444', file=f)
        for row in grid:
            print(''.join(row), file=f)


def trace_outline(segments):
    #outline = defaultdict(list)
    all_points = set()
    for start, d, length, _ in segments:
        row, col = start
        for i in range(length + 1):
            r = row
            c = col
            if d == 'R':
                c += i
            elif d == 'D':
                r += i
            elif d == 'L':
                c -= i
            elif d == 'U':
                r -= i
            #assert (r, c) not in all_points, f"Double point ({r}, {c})"
            all_points.add((r, c))
            #if d in 'UD':
            #    outline[r].append((c, d))
    return all_points

def flood_fill(points, row, col):
    q = [(row, col)]
    points.add((row, col))
    OFF = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    while q:
        r, c = q.pop()
        for dx, dy in OFF:
            nr = r + dx
            nc = c + dy
            if (nr, nc) not in points:
                q.append((nr, nc))
                points.add((nr, nc))


def count_dig(segments, limits):
    all_points = trace_outline(segments)
    start, d, _, _ = segments[0]
    if d == 'R':
        seed_row = start[0] + 1
        seed_col = start[1] + 1
    elif d == 'L':
        seed_row = start[0] - 1
        seed_col = start[1] - 1
    elif d == 'D':
        seed_row = start[0] + 1
        seed_col = start[1] - 1
    elif d == 'U':
        seed_row = start[0] - 1
        seed_col = start[1] + 1
    flood_fill(all_points, seed_row, seed_col)
    return len(all_points)
    """
    total = 0
    m_row, M_row, m_col, M_col = limits
    for row in range(m_row, M_row + 1):
        bounds = sorted(outline[row])
        assert bounds
        prev = bounds[0]
        # If the outline is clockwise, first point on each line is RIGHT or UP
        assert prev[1] == 'U'
        line_points = 1
        for i in range(1, len(bounds)):
            current = bounds[i]
            if prev[1] != 'D' or current[1] != 'U':
                line_points += current[0] - prev[0]
            prev = current
        print(row, line_points)
        print(bounds)
        total += line_points
    return total
    """

def part1(input):
    lines = input.get_valid_lines()
    segments, limits = parse_line_segments(lines)
    #draw(segments, limits)
    #print(segments)
    #print(limits)
    return count_dig(segments, limits)


e.run_tests(1, part1)
e.run_main(1, part1)

def part2(input):
    
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
