#!/usr/bin/env python3

import curses
import intcode
import sys

with open('input15.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

pos = [0, 0]
direct = 1
plan = {'0,0': '.'}
minmax = [0, 0, 0, 0]
counter = 0
shortest_dist = 0

c_left = {
    1: 3,
    2: 4,
    3: 2,
    4: 1
}
c_right = {
    1: 4,
    2: 3,
    3: 1,
    4: 2
}
c_back = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}
pr = {
    1: 'up',
    2: 'down',
    3: 'left',
    4: 'right'
}

oxygen = None

def get_newpos(pos, direct):
    return {
        1: [pos[0], pos[1] - 1],
        2: [pos[0], pos[1] + 1],
        3: [pos[0] - 1, pos[1]],
        4: [pos[0] + 1, pos[1]]
    }[direct]


def update_plan(pos, val):
    global plan
    global minmax

    k = f'{pos[0]},{pos[1]}'
    if val == 0:
        plan[k] = '#'
    elif val == 1:
        plan[k] = '.'
    elif val == 2:
        plan[k] = 'O'

    minmax = [
        min(minmax[0], pos[0]),
        max(minmax[1], pos[0]),
        min(minmax[2], pos[1]),
        max(minmax[3], pos[1])
    ]


def print_plan():
    global scr
    scr.clear()
    for y in range(minmax[2], minmax[3] + 1):
        for x in range(minmax[0], minmax[1] + 1):
            atr = curses.color_pair(0)
            if x == 0 and y == 0:
                atr = curses.color_pair(4)
            elif x == pos[0] and y == pos[1]:
                atr = curses.color_pair(5)
            else:
                k = f'{x},{y}'
                if k in plan:
                    if plan[k] == '.':
                        atr = curses.color_pair(1)
                    elif plan[k] == '#':
                        atr = curses.color_pair(2)
                    elif plan[k] == 'O':
                        atr = curses.color_pair(3)
            scr.move(y - minmax[2], (x - minmax[0]) * 2)
            scr.addstr('  ', atr)
    scr.refresh()


def get_input():
    global direct

    left = c_left[direct]
    leftpos = get_newpos(pos, left)
    k = f'{leftpos[0]},{leftpos[1]}'
    if k not in plan or plan[k] == '.':
        direct = left
        return direct

    forward = get_newpos(pos, direct)
    k = f'{forward[0]},{forward[1]}'
    if k not in plan or plan[k] == '.':
        return direct

    right = c_right[direct]
    rightpos = get_newpos(pos, right)
    k = f'{rightpos[0]},{rightpos[1]}'
    if k not in plan or plan[k] == '.':
        direct = right
        return direct

    direct = c_back[direct]
    return direct


def input_fn():
    inp = get_input()
    return inp


def find_shortest_path():
    q = [(0, 0, 0)]
    qpos = 0
    mindist = {}

    while qpos < len(q):
        x, y, dist = q[qpos]
        qpos += 1

        k = f'{x},{y}'
        if k in mindist and mindist[k] <= dist:
            continue

        if plan[k] == 'O':
            return dist

        mindist[k] = dist
        ndist = dist + 1

        for next in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
            k = f'{next[0]},{next[1]}'
            if k not in plan or plan[k] == '#':
                continue
            if k in mindist and mindist[k] <= ndist:
                continue
            q += [(next[0], next[1], ndist)]
    raise "We didn't find it :-O"


def flood_with_oxygen():
    q = [(oxygen[0], oxygen[1], 0)]
    qpos = 0
    mindist = {}
    farthest = 0

    while qpos < len(q):
        x, y, dist = q[qpos]
        qpos += 1

        k = f'{x},{y}'
        if k in mindist and mindist[k] <= dist:
            continue

        farthest = max(farthest, dist)

        mindist[k] = dist
        ndist = dist + 1

        for next in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
            k = f'{next[0]},{next[1]}'
            if k not in plan or plan[k] == '#':
                continue
            if k in mindist and mindist[k] <= ndist:
                continue
            q += [(next[0], next[1], ndist)]
    return farthest


def output_fn(val):
    global plan
    global pos
    global direct
    global counter
    global scr
    global oxygen
    global shortest_dist

    newpos = get_newpos(pos, direct)
    update_plan(newpos, val)

    if val != 0:
        # position changed
        pos = newpos[:]

    if val == 2:
        oxygen = pos[:]
        shortest_dist = find_shortest_path()

    counter += 1
    if counter == 50000:
        print_plan()
        steps = flood_with_oxygen()
        size = scr.getmaxyx()
        scr.move(size[0] - 1, 0)
        scr.addstr(f'Oxygen at {oxygen}, distance {shortest_dist}, flood in {steps} steps')
        curses.flushinp()
        scr.getch()
        curses.endwin()
        sys.exit(0)

    if counter % 1000 == 0:
        print_plan()


scr = curses.initscr()

try:
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    mach = intcode.IntCode(program)
    mach.run(input_fn, output_fn)
except:
    curses.endwin()
