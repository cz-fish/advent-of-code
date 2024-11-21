#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import deque

e = Env(16)
e.T(""".|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....""", 46, 51)

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
OFFSETS = {
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1),
    UP: (-1, 0),
}
REFLECT = {
    (RIGHT, '\\'): DOWN,
    (RIGHT, '/'): UP,
    (DOWN, '\\'): RIGHT,
    (DOWN, '/'): LEFT,
    (LEFT, '\\'): UP,
    (LEFT, '/'): DOWN,
    (UP, '\\'): LEFT,
    (UP, '/'): RIGHT,
}
SPLIT = {
    (RIGHT, '|'): [UP, DOWN],
    (RIGHT, '-'): [RIGHT],
    (DOWN, '|'): [DOWN],
    (DOWN, '-'): [LEFT, RIGHT],
    (LEFT, '|'): [UP, DOWN],
    (LEFT, '-'): [LEFT],
    (UP, '|'): [UP],
    (UP, '-'): [LEFT, RIGHT],
}


def trace_beam(grid, s_row, s_col, s_d):
    energized = set()
    probed = set()
    q = deque()
    q.append((s_row, s_col, s_d))
    while q:
        state = q.popleft()
        if state in probed:
            continue
        probed.add(state)
        row, col, d = state
        off = OFFSETS[d]
        row += off[0]
        col += off[1]
        while grid.is_in(row, col):
            energized.add((row, col))
            c = grid.get(row, col)
            if c in '/\\':
                # reflect
                q.append((row, col, REFLECT[(d, c)]))
                break
            elif c in '|-':
                # split
                for next_d in SPLIT[(d, c)]:
                    q.append((row, col, next_d))
                break
            elif c != '.':
                assert False, f"Unknown character '{c}' at ({row}, {col}"
            row += off[0]
            col += off[1]
    return energized


def part1(input):
    g = Grid(input.get_valid_lines())
    energized = trace_beam(g, 0, -1, RIGHT)
    return len(energized)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines())
    best = 0
    for row in range(g.h):
        best = max(best, len(trace_beam(g, row, -1, RIGHT)))
        best = max(best, len(trace_beam(g, row, g.w, LEFT)))
    for col in range(g.w):
        best = max(best, len(trace_beam(g, -1, col, DOWN)))
        best = max(best, len(trace_beam(g, g.h, col, UP)))
    return best


e.run_tests(2, part2)
e.run_main(2, part2)
