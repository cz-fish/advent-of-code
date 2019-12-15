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
    #global scr
    #scr.clear()
    for y in range(minmax[2], minmax[3] + 1):
        line = ''
        for x in range(minmax[0], minmax[1] + 1):
            if x == 0 and y == 0:
                line += 'S'
            elif x == pos[0] and y == pos[1]:
                line += 'D'
            else:
                k = f'{x},{y}'
                if k in plan:
                    line += plan[k]
                else:
                    line += ' '
        print(line)
    #scr.refresh()
    #curses.napms(10)


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
    # print(pos, pr[inp])
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
            print(mindist)
            print("min distance to O:", dist)
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


def output_fn(val):
    global plan
    global pos
    global direct
    global counter

    newpos = get_newpos(pos, direct)
    update_plan(newpos, val)

    if val != 0:
        # position changed
        pos = newpos[:]

    if val == 2:
        print('oxygen system at', pos)
        print_plan()
        find_shortest_path()
        sys.exit(0)

    #counter += 1
    #if counter % 100 == 0:
    #    print_plan()
    #    print("-----------------------------------")

    #if counter == 5000:
    #    sys.exit(0)


#scr = curses.initscr()

mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)
