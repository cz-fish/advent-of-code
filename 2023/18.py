#!/usr/bin/python3.8

from pyaoc import Env
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
e.T("""U 2 (#000023)
L 2 (#000022)
U 2 (#000023)
R 5 (#000050)
D 4 (#000041)
L 3 (#000032)""", 26, 26)

#  #######
#  #     #
#  # ### #
#  # # # #
#  ### ###
# 7 + 7 + 7 + 6 + 6 = 33
e.T("""U 4 (#000043)
R 6 (#000060)
D 4 (#000041)
L 2 (#000022)
U 2 (#000023)
L 2 (#000022)
D 2 (#000021)
L 2 (#000022)""", 33, 33)

#  #######
#  #     #
#  # ### #
#  # # # #
#  ### ###
# 7 + 7 + 7 + 6 + 6 = 33
e.T("""R 6 (#000060)
D 4 (#000041)
L 2 (#000022)
U 2 (#000023)
L 2 (#000022)
D 2 (#000021)
L 2 (#000022)
U 4 (#000043)""", 33, 33)

#    ###
#  ### #
#  #   #
#  # ###
#  ###
# 2 * 3 + 3 * 5 = 6 + 15 = 21
e.T("""R 2 ()
D 3 ()
L 2 ()
D 1 ()
L 2 ()
U 3 ()
R 2 ()
U 1 ()""", 21, None)

#  ###
#  # ###
#  #   #
#  ### #
#    ###
# 2 * 3 + 3 * 5 = 6 + 15 = 21
e.T("""R 2 ()
D 1 ()
R 2 ()
D 3 ()
L 2 ()
U 1 ()
L 2 ()
U 3 ()""", 21, None)

#  ### ###
#  # # # #
#  # ### #
#  #     #
#  #######
# 7 + 7 + 7 + 6 + 6 = 33
e.T("""R 2 ()
D 2 ()
R 2 ()
U 2 ()
R 2 ()
D 4 ()
L 6 ()
U 4 ()""", 33, None)


def parse_line_segments(lines, for_part2):
    row = 0
    col = 0
    m_row = 0
    M_row = 0
    m_col = 0
    M_col = 0
    segments = []
    directions = {
        0: 'R',
        1: 'D',
        2: 'L',
        3: 'U',
    }
    for ln in lines:
        d, l, c = ln.split()
        if for_part2:
            assert c.startswith('(#') and c.endswith(')')
            color = int(c[2:-1], 16)
            d_index = color & 0xf
            assert d_index in directions
            d = directions[d_index]
            length = color // 0x10
        else:
            assert c.startswith('(') and c.endswith(')')
            length = int(l)
        segments.append(((row, col), d, length))
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

### -- visualisation
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

### -- end visualisation

### -- flood fill solution

def trace_outline(segments):
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
            all_points.add((r, c))
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

### -- end flood fill solution

### -- BSP solution (not working)

def line_coords(line):
    start, d, length = line
    if d == 'R':
        horizontal = True
        min_row = start[0]
        max_row = start[0]
        min_col = start[1]
        max_col = start[1] + length
    elif d == 'D':
        horizontal = False
        min_row = start[0]
        max_row = start[0] + length
        min_col = start[1]
        max_col = start[1]
    elif d == 'L':
        horizontal = True
        min_row = start[0]
        max_row = start[0]
        min_col = start[1] - length
        max_col = start[1]
    elif d == 'U':
        horizontal = False
        min_row = start[0] - length
        max_row = start[0]
        min_col = start[1]
        max_col = start[1]
    return horizontal, min_row, max_row, min_col, max_col

def end_point(line):
    start, d, length = line
    if d == 'R':
        return start[0], start[1] + length
    elif d == 'D':
        return start[0] + length, start[1]
    elif d == 'L':
        return start[0], start[1] - length
    elif d == 'U':
        return start[0] - length, start[1]

def partition_lines(lines):
    assert lines
    left = []
    right = []
    _, d, _ = lines[0]
    end = end_point(lines[0])
    horizontal, min_row, max_row, min_col, max_col = line_coords(lines[0])
    for i in range(1, len(lines)):
        _, lmin_row, lmax_row, lmin_col, lmax_col = line_coords(lines[i])
        if end == lines[i][0]:
            # next line connects to current line
            if (d == 'R' and lmax_row > min_row) or \
               (d == 'D' and lmin_col < min_col) or \
               (d == 'L' and lmin_row < min_row) or \
               (d == 'U' and lmax_col > min_col):
                # entire line on the right side
                right.append(lines[i])
            else:
                # entire line on the left side
                left.append(lines[i])
        elif (d == 'R' and lmax_row < min_row) or \
           (d == 'D' and lmin_col > max_col) or \
           (d == 'L' and lmin_row > max_row) or \
           (d == 'U' and lmax_col < min_col):
            # entire line on the left side
            left.append(lines[i])
        elif (d == 'R' and lmin_row >= max_row) or \
             (d == 'D' and lmax_col <= min_col) or \
             (d == 'L' and lmax_row <= min_row) or \
             (d == 'U' and lmin_col >= max_col):
            # entire line on the right side
            right.append(lines[i])
        else:
            # split line in 2
            _, ld, _ = lines[i]
            if d == 'R':
                # horizontal line cutting a vertical one at row `min_row`
                if ld == 'U':
                    left.append(((min_row - 1, lmin_col), ld, min_row - lmin_row - 1))
                    right.append(((lmax_row, lmin_col), ld, lmax_row - min_row))
                elif ld == 'D':
                    left.append(((lmin_row, lmin_col), ld, min_row - lmin_row - 1))
                    right.append(((min_row, lmin_col), ld, lmax_row - min_row))
                else:
                    assert False
            elif d == 'D':
                # vertical line cutting a horizontal one at col `min_col`
                if ld == 'L':
                    left.append(((lmin_row, lmax_col), ld, lmax_col - min_col - 1))
                    right.append(((lmin_row, min_col), ld, min_col - lmin_col))
                elif ld == 'R':
                    left.append(((lmin_row, min_col), ld, lmax_col - min_col - 1))
                    right.append(((lmin_row, lmin_col), ld, min_col - lmin_col))
                else:
                    assert False
            elif d == 'L':
                # horizontal line cutting a vertical one at row `min_row`
                if ld == 'U':
                    left.append(((lmax_row, lmin_col), ld, lmax_row - min_row - 1))
                    right.append(((min_row, lmin_col), ld, min_row - lmin_row))
                elif ld == 'D':
                    left.append(((min_row + 1, lmin_col), ld, lmax_row - min_row - 1))
                    right.append(((lmin_row, lmin_col), ld, min_row - lmin_row))
                else:
                    assert False
            elif d == 'U':
                # vertical line cutting a horizontal one at col `min_col`
                if ld == 'L':
                    left.append(((lmin_row, min_col - 1), ld, min_col - lmin_col - 1))
                    right.append(((lmin_row, lmax_col), ld, lmax_col - min_col))
                elif ld == 'R':
                    left.append(((lmin_row, lmin_col), ld, min_col - lmin_col - 1))
                    right.append(((lmin_row, min_col), ld, lmax_col - min_col))
                else:
                    assert False
    return left, right


def recursive_bsp(lines, left, top, right, bottom, inside, depth, path):
    ind = ' ' * depth
    #print(f"{ind}BSP of {len(lines)} lines {lines}. left={left} top={top} right={right} bottom={bottom} inside={inside}")
    if not lines:
        # end of BSP descent
        if not inside:
            return 0
        assert all([x is not None for x in [left, top, right, bottom]]), f"Region not closed. {left} {top} {right} {bottom}, path {path}"
        # internal area
        assert right >= left
        assert bottom >= top
        area = (right - left + 1) * (bottom - top + 1)
        #print(f"{ind} -> area {area}")
        return area
    # partition all other lines by the first line
    left_lines, right_lines = partition_lines(lines)
    start, d, length = lines[0]
    path = path + f"({start} {d})"
    # assuming the path is clockwise, left side of the line is outside and right side is inside
    # The line itself should be included in the right half, and excluded from the left half
    total = 0
    if d == 'R':
        # above is 'left side', below is 'right side'
        total += recursive_bsp(left_lines, left, top, right, start[0] - 1, False, depth + 1, path)
        total += recursive_bsp(right_lines, left, start[0], right, bottom, True, depth + 1, path)
    elif d == 'D':
        # right is 'left side', left is 'right side'
        total += recursive_bsp(left_lines, start[1] + 1, top, right, bottom, False, depth + 1, path)
        total += recursive_bsp(right_lines, left, top, start[1], bottom, True, depth + 1, path)
    elif d == 'L':
        # below is 'left side', above is 'right side'
        total += recursive_bsp(left_lines, left, start[0] + 1, right, bottom, False, depth + 1, path)
        total += recursive_bsp(right_lines, left, top, right, start[0], True, depth + 1, path)
    elif d == 'U':
        # left is 'left side', right is 'right side'
        total += recursive_bsp(left_lines, left, top, start[1] - 1, bottom, False, depth + 1, path)
        total += recursive_bsp(right_lines, start[1], top, right, bottom, True, depth + 1, path)
    return total

### -- end BSP solution

### -- XOR painting solution (not working)

def xor_paint(segments, limits):
    total = 0
    _, max_row, _, max_col = limits
    print(f"max row {max_row}, max col {max_col}")
    for segment in segments:
        start, d, length = segment
        if d == 'R':
            under = (length - 1) * (max_row - start[0] + 1)
            print(f"Line {segment} adds {under}")
            total += under
        elif d == 'D':
            print(f"Line {segment} adds its length {length + 1}")
            total += length + 1
        #    right = length * (max_col - start[1])
        #    print(f"Line {segment} subtracts {right}")
        #    total -= right
        elif d == 'L':
            under = (length - 1) * (max_row - start[0])
            print(f"Line {segment} subtracts {under}")
            total -= under
        elif d == 'U':
            print(f"Line {segment} adds its length {length + 1}")
            total += length + 1
        #    right = length * (max_col - start[1] + 1)
        #    print(f"Line {segment} adds {right}")
        #    total += right
    return total

### -- end XOR painting solution

### -- Rectangle splitting solution

# Corner / point classification
TL = 0  # topleft of a square ◤
TR = 1  # topright of a square ◥
BL = 2  # bottomleft of a square ◣
BR = 3  # bottomright of a square ◢
VL = 4  # vertical with inside on the left
VR = 5  # vertical with inside on the right


def extract_points(segments):
    scanlines = defaultdict(list)
    # find and classify all corners
    corner_types = {
        'UR': TL,
        'UL': TR,
        'DR': BL,
        'DL': BR,
        'RU': BR,
        'RD': TR,
        'LU': BL,
        'LD': TL,
    }
    for i in range(len(segments)):
        point, this_segment_dir, _ = segments[i]
        _, prev_segment_dir, _ = segments[i-1]
        type = corner_types[prev_segment_dir + this_segment_dir]
        scanlines[point[0]].append((point[1], type))

    # add all vertical line split points
    for row in scanlines.keys():
        for segment in segments:
            start, d, length = segment
            horizontal, min_row, max_row, min_col, max_col = line_coords(segment)
            if horizontal:
                # not a vertical segment
                continue
            if max_row <= row or min_row >= row:
                # not intersected by scanline on row `row`
                continue
            if d == 'U':
                type = VR
            else:
                type = VL
            scanlines[row].append((min_col, type))

    # sort each scanline from left to right
    for row in scanlines.keys():
        scanlines[row].sort()
    return scanlines


def point_scanlines(segments):
    scanlines = extract_points(segments)
    rows = sorted(list(scanlines.keys()))
    rectangles = []
    for i in range(len(rows)):
        row = rows[i]
        if i < len(rows) - 1:
            next_row = rows[i+1]
        else:
            # For the last row, there is nothing more underneath
            next_row = row
        height = next_row - row

        scanline = scanlines[row]
        first_type = scanline[0][1]
        assert first_type in [TL, BL, VR], f"Incorrect type of first point on scanline {row} -> {first_type}"

        inside = False
        bottom = False
        last_col_counted = 0
        for point_idx in range(len(scanline)):
            prev_col, prev_type = scanline[point_idx - 1]
            col, type = scanline[point_idx]
            width = col - prev_col + 1 - last_col_counted
            last_col_counted = 0
            if inside:
                rectangles.append((prev_col, col, row, next_row - 1, False))
            elif bottom:
                rectangles.append((prev_col, col, row, row, True))
            if type == VL:
                assert inside, "Got vertical left while not being inside"
                inside = False
            elif type == VR:
                assert not inside, "Got vertical right while being inside"
                inside = True
            elif type == TL or type == TR:
                inside = not inside
                if type == TL and not inside:
                    bottom = True
                    last_col_counted = 1
                elif type == TR and inside:
                    bottom = False
            # no change in `inside`, but potential change in `bottom`
            elif type == BL and not inside:
                assert not bottom
                bottom = True
                last_col_counted = 1
            elif type == BR and not inside:
                assert bottom
                bottom = False
            #else: # no change in either `inside` or `bottom`
        assert not inside, "Finished scanline and still inside"
    total = 0
    prev_row = None
    prev_col = None
    prev_thin = None
    for rect in rectangles:
        left, right, top, bottom, thin = rect
        # remove overlap. The only possible overlap can be between two
        # adjacent rectangles on the same vertical position, and they can
        # overlap by 1 pixel
        if prev_row == top and prev_col == left:
            if prev_thin:
                # fix the overlap by removing from the left rectangle
                total -= 1
            else:
                # fix the overlap by removing from the right rectangle
                left += 1
        area = (right - left + 1) * (bottom - top + 1)
        total += area
        prev_row = top
        prev_col = right
        prev_thin = thin
    return total

### -- end rectangle splitting solution

def calculate_area(segments, limits):
    if False:
        # Binary space partitioning idea
        # not implemented correctly
        return recursive_bsp(segments, None, None, None, None, False, 0, "")
    if False:
        # Inverting right and bottom areas idea
        # not implemented correctly
        return xor_paint(segments, limits)
    # Rectangle splitting solution
    # works
    return point_scanlines(segments)

def part1(input):
    lines = input.get_valid_lines()
    segments, limits = parse_line_segments(lines, False)

    # Draw path to a picture file
    #draw(segments, limits)

    # Flood fill solution. Good enough for part 1
    #return count_dig(segments, limits)

    # Solution for part 2 also works for part 1
    return calculate_area(segments, limits)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    segments, limits = parse_line_segments(lines, True)
    return calculate_area(segments, limits)


e.run_tests(2, part2)
e.run_main(2, part2)
