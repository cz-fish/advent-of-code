#!/usr/bin/env python3

import intcode

with open('input13.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

def input_fn():
    pass


def get_board(output):
    board = {}
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    for i in range(0,len(output),3):
        x = output[i]
        y = output[i+1]
        block = output[i+2]
        board[(x, y)] = block
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    return board, minx, maxx, miny, maxy


mach = intcode.IntCode(program)
mach.run(input_fn)
board, minx, maxx, miny, maxy = get_board(mach.output)
width = maxx - minx + 1
height = maxy - miny + 1

with open('13-board.xpm', 'wt') as f:
    f.writelines([
        "! XPM2\n",
        f"{width} {height} 5 1\n",
        "0 c #000000\n",
        "1 c #aaaaaa\n",
        "2 c #b46666\n",
        "3 c #5070bb\n",
        "4 c #50a050\n"
        ])
    for y in range(miny, maxy+1):
        line = ''
        for x in range(minx, maxx+1):
            k = (x, y)
            if k not in board:
                v = 0
            else:
                v = board[k]
            line += str(v)
        f.write(line + '\n')

