#!/usr/bin/python3.8

from aoc import Input, Grid
from collections import defaultdict, deque

inp = Input('input11.txt', ["""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""])

# inp.use_test(0)

grid = Grid(inp.get_lines())
print(grid.w, grid.h)


def game_step(grid):
    gr = Grid([''.join(grid.grid[r]) for r in range(grid.h)])
    changed = 0
    for r in range(gr.h):
        for c in range(gr.w):
            p = gr.get(r, c)
            if p == '.':
                continue
            nc = gr.neighbors8(r, c)
            count = sum([1 for a, b in nc if gr.get(a, b) == '#'])
            if p == 'L' and count == 0:
                grid.grid[r][c] = '#'
                changed += 1
            elif p == '#' and count >= 4:
                grid.grid[r][c] = 'L'
                changed += 1
    return changed


# Part 1
"""
while True:
    changed = game_step(grid)
    if changed == 0:
        count = sum([sum(
            [1 for c in r if c == '#'])
            for r in grid.grid])
        print(f"Part 1: occupied {count}")
        break
"""


# Part 2

def find_seats(grid):
    visible_seats = defaultdict(list)
    for r in range(grid.h):
        for c in range(grid.w):
            if grid.get(r, c) == '.':
                continue
            probe = deque()
            for step in [(-1,-1), (-1,0), (-1,1),
                         (0,-1), (0,1),
                         (1,-1), (1,0), (1,1)]:
                probe.append([r, c, step])
            while probe:
                y, x, d = probe.popleft()
                y += d[0]
                x += d[1]
                if grid.is_in(y, x):
                    s = grid.get(y, x)
                    if s == '.':
                        # keep going
                        probe.append([y, x, d])
                    else:
                        visible_seats[(r, c)] += [(y, x)]
    return visible_seats


def game_step_part2(grid, vis_seats):
    gr = Grid([''.join(grid.grid[r]) for r in range(grid.h)])
    changed = 0
    for r in range(gr.h):
        for c in range(gr.w):
            p = gr.get(r, c)
            if p == '.':
                continue
            count = sum([1 for y, x in vis_seats[(r, c)] if gr.get(y, x) == '#'])
            if p == 'L' and count == 0:
                grid.grid[r][c] = '#'
                changed += 1
            elif p == '#' and count >= 5:
                grid.grid[r][c] = 'L'
                changed += 1
    return changed


vis_seats = find_seats(grid)
while True:
    changed = game_step_part2(grid, vis_seats)
    if changed == 0:
        count = sum([sum(
            [1 for c in r if c == '#'])
            for r in grid.grid])
        print(f"Part 2: occupied {count}")
        break
#print(vis_seats)
#print(vis_seats[(7, 7)])

