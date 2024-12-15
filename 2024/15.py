#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque

e = Env(15)
e.T("""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""", 10092, 9021)

e.T("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""", 2028, None)

e.T("""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""", None, 105 + 207 + 306)


def find_robot(g):
    for row in range(g.h):
        for col in range(g.w):
            if g.get(row, col) == '@':
                return row, col
    assert False, "No robot found"


def push(g, r, c, dr, dc, symbol):
    nr = r + dr
    nc = c + dc
    what = g.get(nr, nc)
    if what == '#':
        return False
    if what == '.':
        moved = True
    else:
        moved = push(g, nr, nc, dr, dc, what)
    if moved:
        g.grid[nr][nc] = symbol
    return moved


def push_vertically(g, r, c, dr):
    q = deque()
    q.append((r+dr, c))
    moved_boxes = set()
    while q:
        tr, tc = q.popleft()
        what = g.get(tr, tc)
        if what == '#':
            # move is blocked
            return False
        if what == '.':
            continue
        if what == '[':
            box_left = tc
        elif what == ']':
            box_left = tc - 1
        else:
            assert False, f"What did we bump into? {what} at {tr} {tc}"

        if (tr, box_left) in moved_boxes:
            continue
        moved_boxes.add((tr, box_left))
        q.append((tr + dr, box_left))
        q.append((tr + dr, box_left + 1))
    # move is valid; now move all the boxes
    for br, bc in moved_boxes:
        g.grid[br][bc] = '.'
        g.grid[br][bc+1] = '.'
    for br, bc in moved_boxes:
        g.grid[br+dr][bc] = '['
        g.grid[br+dr][bc+1] = ']'

    return True


def push_boxes(g, robot, instr, careful_vertically=False):
    dirs = {
        '<': (0, -1),
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
    }
    r, c = robot
    for i in instr:
        dr, dc = dirs[i]
        if not careful_vertically or dr == 0:
            # single sized boxes, or horizontal movement
            moved = push(g, r, c, dr, dc, '@')
        else:
            # vertical movement with double sized boxes
            moved = push_vertically(g, r, c, dr)
        if moved:
            g.grid[r][c] = '.'
            r += dr
            c += dc
            g.grid[r][c] = '@'


def print_grid(g):
    for r in range(g.h):
        print(''.join(g.grid[r]))


def count_grid_score(g):
    total = 0
    for r in range(g.h):
        for c in range(g.w):
            if g.get(r, c) in 'O[':
                total += 100 * r + c
    return total


def part1(input):
    groups = input.get_groups()
    g = Grid(groups[0])
    instr = ''.join(groups[1])
    robot = find_robot(g)
    push_boxes(g, robot, instr)
    print_grid(g)
    return count_grid_score(g)


e.run_tests(1, part1)
e.run_main(1, part1)


def expand_grid(g):
    lines = []
    expand = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }
    for r in range(g.h):
        lines.append(''.join([expand[c] for c in g.grid[r]]))
    return Grid(lines)


def part2(input):
    groups = input.get_groups()
    g = expand_grid(Grid(groups[0]))
    instr = ''.join(groups[1])
    robot = find_robot(g)
    push_boxes(g, robot, instr, careful_vertically=True)
    print_grid(g)
    return count_grid_score(g)


e.run_tests(2, part2)
e.run_main(2, part2)
