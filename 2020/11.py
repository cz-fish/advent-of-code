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

orig_grid = Grid(inp.get_lines())


def surrounding_seats_part1(grid):
    visible_seats = defaultdict(list)
    for r in range(grid.h):
        for c in range(grid.w):
            if grid.get(r, c) == '.':
                continue
            visible_seats[(r, c)] = grid.neighbors8(r, c)
    return visible_seats


def surrounding_seats_part2(grid):
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


def game_step(grid, vis_seats, threshold):
    updates = {}
    for r in range(grid.h):
        for c in range(grid.w):
            p = grid.get(r, c)
            if p == '.':
                continue
            count = sum([1 for y, x in vis_seats[(r, c)] if grid.get(y, x) == '#'])
            if p == 'L' and count == 0:
                updates[(r, c)] = '#'
            elif p == '#' and count >= threshold:
                updates[(r, c)] = 'L'
    changed = len(updates)
    for (r, c), v in updates.items():
        grid.grid[r][c] = v
    return changed


def count_occupied(grid, vis_seats, threshold):
    while True:
        changed = game_step(grid, vis_seats, threshold)
        if changed == 0:
            count = sum([sum(
                [1 for c in r if c == '#'])
                for r in grid.grid])
            return count

grid = Grid.copygrid(orig_grid)
occupied = count_occupied(grid, surrounding_seats_part1(grid), 4)
print(f"Part 1: occupied {occupied}")

grid = Grid.copygrid(orig_grid)
occupied = count_occupied(grid, surrounding_seats_part2(grid), 5)
print(f"Part 2: occupied {occupied}")
