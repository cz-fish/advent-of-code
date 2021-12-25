#!/usr/bin/python3.8

from aoc import Env, Grid

e = Env(25)

def eT(*args):
    pass

# This test won't finish
eT("""...>...
.......
......>
v.....>
......>
.......
..vvv..""", 0, None)

e.T("""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""", 58, None)


def find_herds(grid):
    hori = set()
    ver = set()
    for row in range(grid.h):
        for col in range(grid.w):
            c = grid.grid[row][col]
            if c == '>':
                hori.add((row, col))
            elif c == 'v':
                ver.add((row, col))
    return hori, ver


def move(movable, hori, ver, herd, needed, step, width, height):
    unblocked = set()
    still_movable = set()
    for m in movable:
        target = ((m[0] + step[0]) % height, (m[1] + step[1]) % width)
        if target not in hori and target not in ver:
            unblocked.add(m)
            herd.add(target)
            still_movable.add(target)
        else:
            needed[target] = m
    for m in unblocked:
        herd.remove(m)
    return unblocked, still_movable


def add_unblocked(movable, unblocked, needed):
    for t, m in list(needed.items()):
        if t in unblocked:
            movable.add(m)
            del needed[t]


def print_herd(hori, ver, width, height):
    s = [
        ['.' for _ in range(width)]
        for _ in range(height)
    ]
    for r, c in hori:
        s[r][c] = '>'
    for r, c in ver:
        s[r][c] = 'v'
    for ln in s:
        print(''.join(ln))


def part1(input):
    g = Grid(input.get_valid_lines())
    hori, ver = find_herds(g)
    movable_h = hori.copy()
    movable_v = ver.copy()
    needed_h = {}
    needed_v = {}
    unblocked_h = set()
    unblocked_v = set()
    step = 0
    while True:
        add_unblocked(movable_h, unblocked_h, needed_h)
        unblocked_v, movable_h = move(movable_h, hori, ver, hori, needed_h, (0, 1), g.w, g.h)
        add_unblocked(movable_h, unblocked_v, needed_h)
        add_unblocked(movable_v, unblocked_v, needed_v)
        unblocked_h, movable_v = move(movable_v, hori, ver, ver, needed_v, (1,0), g.w, g.h)
        add_unblocked(movable_v, unblocked_h, needed_v)
        step += 1
        if not unblocked_v and not unblocked_h:
            break
    return step


e.run_tests(1, part1)
e.run_main(1, part1)
