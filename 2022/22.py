#!/usr/bin/python3.8

from pyaoc import Env, Grid

side_none = 0
side_front = 1
side_left = 2
side_right = 3
side_back = 4
side_top = 5
side_bottom = 6

rot_none = 0
rot_cw = 1
rot_ccw = 3
rot_180 = 2

edge_top = 0
edge_right = 1
edge_bottom = 2
edge_left = 3

edge_map = {
    (side_front, edge_top): (side_top, edge_bottom),
    (side_front, edge_left): (side_left, edge_right),
    (side_front, edge_right): (side_right, edge_left),
    (side_front, edge_bottom): (side_bottom, edge_top),

    (side_top, edge_top): (side_back, edge_top),
    (side_top, edge_left): (side_left, edge_top),
    (side_top, edge_right): (side_right, edge_top),
    (side_top, edge_bottom): (side_front, edge_top),

    (side_left, edge_top): (side_top, edge_left),
    (side_left, edge_left): (side_back, edge_right),
    (side_left, edge_right): (side_front, edge_left),
    (side_left, edge_bottom): (side_bottom, edge_left),

    (side_right, edge_top): (side_top, edge_right),
    (side_right, edge_left): (side_front, edge_right),
    (side_right, edge_right): (side_back, edge_left),
    (side_right, edge_bottom): (side_bottom, edge_right),

    (side_bottom, edge_top): (side_front, edge_bottom),
    (side_bottom, edge_left): (side_left, edge_bottom),
    (side_bottom, edge_right): (side_right, edge_bottom),
    (side_bottom, edge_bottom): (side_back, edge_bottom),

    (side_back, edge_top): (side_top, edge_top),
    (side_back, edge_left): (side_right, edge_right),
    (side_back, edge_right): (side_left, edge_left),
    (side_back, edge_bottom): (side_bottom, edge_bottom),
}

# FIXME: hardcoding the wrapping of the input into the param for now
e = Env(22, raw_lines=True, param={
    'square': 50,
    'shape': [
        [(side_none, rot_none), (side_top, rot_none), (side_right, rot_ccw)],
        [(side_none, rot_none), (side_front, rot_none), (side_none, rot_none)],
        [(side_left, rot_ccw), (side_bottom, rot_none), (side_none, rot_none)],
        [(side_back, rot_ccw), (side_none, rot_none), (side_none, rot_none)]
    ]
})
e.T("""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""", 6032, 5031, param={
    'square': 4,
    'shape': [
        [(side_none, rot_none), (side_none, rot_none), (side_top, rot_none), (side_none, rot_none)],
        [(side_back, rot_none), (side_left, rot_none), (side_front, rot_none), (side_none, rot_none)],
        [(side_none, rot_none), (side_none, rot_none), (side_bottom, rot_none), (side_right, rot_cw)]
    ]
})

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

sign = {
    RIGHT: '>',
    DOWN: 'v',
    LEFT: '<',
    UP: '^'
}


def find_start(grid):
    for col in range(grid.w):
        if grid.get(0, col) == '.':
            return 0, col
    assert False, "no dot on the top line"


def next_pos_part1(grid, pos, facing, _param):
    if facing == RIGHT:
        d = (0, 1)
    elif facing == DOWN:
        d = (1, 0)
    elif facing == LEFT:
        d = (0, -1)
    elif facing == UP:
        d = (-1, 0)
    while True:
        pos = ((pos[0] + d[0]) % grid.h, (pos[1] + d[1]) % grid.w)
        if pos[1] >= len(grid.grid[pos[0]]):
            continue
        if grid.get(pos[0], pos[1]) != ' ':
            break
    return pos, facing


def walk(grid, steps, start, facing, next_pos, param):
    pos = start
    grid.grid[pos[0]][pos[1]] = sign[facing]
    dist = 0
    turn = 0
    for c in steps + '.':
        if c >= '0' and c <= '9':
            dist = 10 * dist + ord(c) - ord('0')
            continue
        if c == 'L':
            turn = -1
        elif c == 'R':
            turn = 1
        elif c != '.':
            assert False, f"unknown character '{c}'"
        # walk, then turn
        for _ in range(dist):
            go, new_face = next_pos(grid, pos, facing, param)
            try:
                if grid.get(go[0], go[1]) == '#':
                    # hit a wall
                    break
            except IndexError:
                print(pos, facing, go, new_face)
                raise
            pos = go
            facing = new_face
            grid.grid[pos[0]][pos[1]] = sign[facing]

        facing = (facing + turn) % 4
        grid.grid[pos[0]][pos[1]] = sign[facing]
        turn = 0
        dist = 0
    return pos[0], pos[1], facing


def get_grid_and_steps(input):
    parts = input.get_groups()
    assert len(parts) == 2
    grid = Grid(parts[0], rectangular=False)
    assert len(parts[1]) == 1
    steps = parts[1][0]
    return grid, steps


def part1(input):
    grid, steps = get_grid_and_steps(input)
    start = find_start(grid)
    end = walk(grid, steps, start, RIGHT, next_pos_part1, {})
    #for r in range(grid.h):
    #    print(''.join(grid.grid[r]))
    return (end[0] + 1) * 1000 + (end[1] + 1) * 4 + end[2]


e.run_tests(1, part1)
e.run_main(1, part1)

## --- part 2 ---

def seam_points(side, a_x, a_y, a_rot, a_edge, b_x, b_y, b_rot, b_edge, flip_horizontal):
    source_left = a_x * side
    source_top = a_y * side
    tgt_left = b_x * side
    tgt_top = b_y * side
    # Rotation values are amounts of 90-degree clockwise rotations
    # Edge values go clockwise from top
    a_edge = (a_edge + a_rot) % 4
    b_edge = (b_edge + b_rot) % 4

    if a_edge == edge_top:
        edge_start = (source_left, source_top)
        overstep_start = (source_left, source_top - 1)
        d_edge_x = 1
        d_edge_y = 0
    elif a_edge == edge_right:
        edge_start = (source_left + side - 1, source_top)
        overstep_start = (source_left + side, source_top)
        d_edge_x = 0
        d_edge_y = 1
    elif a_edge == edge_bottom:
        edge_start = (source_left, source_top + side - 1)
        overstep_start = (source_left, source_top + side)
        d_edge_x = 1
        d_edge_y = 0
    elif a_edge == edge_left:
        edge_start = (source_left, source_top)
        overstep_start = (source_left - 1, source_top)
        d_edge_x = 0
        d_edge_y = 1

    invert = (b_rot == rot_cw or b_rot == rot_180)
    if flip_horizontal and b_edge in [edge_top, edge_bottom]:
        invert = not invert

    if b_edge == edge_top:
        facing = DOWN
        d_wrap_y = 0
        if invert:
            wrap_start = (tgt_left + side - 1, tgt_top)
            d_wrap_x = -1
        else:
            wrap_start = (tgt_left, tgt_top)
            d_wrap_x = 1
    elif b_edge == edge_right:
        facing = LEFT
        d_wrap_x = 0
        if invert:
            wrap_start = (tgt_left + side - 1, tgt_top + side - 1)
            d_wrap_y = -1
        else:
            wrap_start = (tgt_left + side - 1, tgt_top)
            d_wrap_y = 1
    elif b_edge == edge_bottom:
        facing = UP
        d_wrap_y = 0
        if invert:
            wrap_start = (tgt_left + side - 1, tgt_top + side - 1)
            d_wrap_x = -1
        else:
            wrap_start = (tgt_left, tgt_top + side - 1)
            d_wrap_x = 1
    elif b_edge == edge_left:
        facing = RIGHT
        d_wrap_x = 0
        if invert:
            wrap_start = (tgt_left, tgt_top + side - 1)
            d_wrap_y = -1
        else:
            wrap_start = (tgt_left, tgt_top)
            d_wrap_y = 1

    return edge_start, overstep_start, d_edge_x, d_edge_y, wrap_start, d_wrap_x, d_wrap_y, facing


def make_seams(param):
    square = param['square']
    sides = param['shape']

    side_map = {}
    for y in range(len(sides)):
        for x in range(len(sides[y])):
            side, rot = sides[y][x]
            if side == side_none:
                continue
            assert side not in side_map, f"multiple definition of side {side}"
            side_map[side] = (x, y, rot)
    assert len(side_map) == 6, f"did not get 6 sides"

    seams = {}
    for side in range(1, 7):
        x, y, rot = side_map[side]
        for edge in range(4):
            matching_side, matching_edge = edge_map[(side, edge)]
            match_x, match_y, match_rot = side_map[matching_side]

            flip_horizontal = (side == side_back and matching_side == side_bottom) \
                or (side == side_back and matching_side == side_top) \
                or (side == side_top and matching_side == side_back) \
                or (side == side_bottom and matching_side == side_back)

            seam = seam_points(square, x, y, rot, edge, match_x, match_y, match_rot, matching_edge, flip_horizontal)
            edge_start, overstep_start, d_edge_x, d_edge_y, wrap_start, d_wrap_x, d_wrap_y, facing = seam

            if overstep_start == wrap_start and d_edge_x == d_wrap_x and d_edge_y == d_wrap_y:
                # this seam is a no-op
                continue

            for i in range(square):
                seams[(
                    (overstep_start[1] + d_edge_y * i, overstep_start[0] + d_edge_x * i),
                    (edge_start[1] + d_edge_y * i, edge_start[0] + d_edge_x * i)
                )] = ((wrap_start[1] + d_wrap_y * i, wrap_start[0] + d_wrap_x * i), facing)
    return seams


def get_hardcoded_seams():
    seams = {}
    def one_seam(e_s, o_s, d_x, d_y, w_s, dw_x, dw_y, f):
        nonlocal seams
        for i in range(50):
            seams[(
                (o_s[0] + d_y * i, o_s[1] + d_x * i),
                (e_s[0] + d_y * i, e_s[1] + d_x * i)
            )] = ((w_s[0] + dw_y * i, w_s[1] + dw_x * i), f)

    one_seam((0, 50), (-1, 50), 1, 0, (150, 0), 0, 1, RIGHT)
    one_seam((0, 100), (-1, 100), 1, 0, (199, 0), 1, 0, UP)
    one_seam((0, 149), (0, 150), 0, 1, (149, 99), 0, -1, LEFT)
    one_seam((49, 100), (50, 100), 1, 0, (50, 99), 0, 1, LEFT)
    one_seam((50, 99), (50, 100), 0, 1, (49, 100), 1, 0, UP)
    one_seam((149, 99), (149, 100), 0, -1, (0, 149), 0, 1, LEFT)
    one_seam((149, 50), (150, 50), 1, 0, (150, 49), 0, 1, LEFT)
    one_seam((150, 49), (150, 50), 0, 1, (149, 50), 1, 0, UP)
    one_seam((199, 0), (200, 0), 1, 0, (0, 100), 1, 0, DOWN)
    one_seam((150, 0), (150, -1), 0, 1, (0, 50), 1, 0, DOWN)
    one_seam((149, 0), (149, -1), 0, -1, (0, 50), 0, 1, RIGHT)
    one_seam((100, 0), (99, 0), 1, 0, (50, 50), 0, 1, RIGHT)
    one_seam((50, 50), (50, 49), 0, 1, (100, 0), 1, 0, DOWN)
    one_seam((0, 50), (0, 49), 0, 1, (149, 0), 0, -1, RIGHT)

    return seams


def next_pos_part2(grid, pos, facing, seams):
    if facing == RIGHT:
        d = (0, 1)
    elif facing == DOWN:
        d = (1, 0)
    elif facing == LEFT:
        d = (0, -1)
    elif facing == UP:
        d = (-1, 0)

    npos = ((pos[0] + d[0]), (pos[1] + d[1]))
    if (npos, pos) in seams:
        # wrap around a seam
        to, face = seams[(npos, pos)]
        print(f"seam pass: {pos} -> {npos} facing {facing} switch to {to} facing {face}")
        return to, face
    # continue on the same side
    return npos, facing


def part2(input):
    grid, steps = get_grid_and_steps(input)
    start = find_start(grid)

    seams = make_seams(e.get_param())
    if e.get_param()['square'] == 50:
        hardcoded_seams = get_hardcoded_seams()
        # TODO compare seams and hardcoded seams to find the error
        # in the calculated seams
        print(f"seams {len(seams)}, hardcoded {len(hardcoded_seams)}")
        seams = hardcoded_seams

    for k,v in seams.items():
        print(f"{k} -> {v}")
    print("-----")
    end = walk(grid, steps, start, RIGHT, next_pos_part2, seams)
    for r in range(grid.h):
        print(''.join(grid.grid[r]))
    return (end[0] + 1) * 1000 + (end[1] + 1) * 4 + end[2]


e.run_tests(2, part2)
e.run_main(2, part2)

# 25316 too low
