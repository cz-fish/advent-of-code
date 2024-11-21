#!/usr/bin/python3.8

from pyaoc import Env, Grid
from collections import deque
import heapq

e = Env(15)
e.T("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""", 40, 315)


def find_safest_path_bfs(grid):
    best_cost = [[None for _ in range(grid.w)] for _ in range(grid.h)]
    q = deque()
    q.append((0, 0, 0))
    while q:
        y, x, cost = q.popleft()
        if best_cost[y][x] is not None and best_cost[y][x] <= cost:
            continue
        best_cost[y][x] = cost
        for r, s in grid.neighbors4(y, x):
            q.append((r, s, cost + grid.get(r, s)))

    return best_cost[grid.h-1][grid.w-1]


def make_larger_grid(grid, repeats):
    lg = [[0 for _ in range(grid.w * repeats)] for _ in range(grid.h * repeats)]
    for x in range(repeats):
        for y in range(repeats):
            for r in range(grid.h):
                for c in range(grid.w):
                    a = c + x * grid.w
                    b = r + y * grid.h
                    o = x + y
                    lg[b][a] = (grid.get(r, c) + o - 1) % 9 + 1

    long_lines = []
    for row in lg:
        long_lines += [''.join(str(x) for x in row)]
    return Grid(long_lines, ints=True)


def find_safest_path_greedy(grid):
    q = [(0, 0, 0)]
    tgx = grid.w - 1
    tgy = grid.h - 1
    visited = set()
    while q:
        cost, y, x = heapq.heappop(q)
        if (y, x) in visited:
            continue
        if x == tgx and y == tgy:
            return cost
        visited.add((y, x))
        for r, s in grid.neighbors4(y, x):
            if (r, s) not in visited:
                heapq.heappush(q, (cost + grid.get(r, s), r, s))
    return 0


def part1(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    #return find_safest_path_bfs(grid)
    return find_safest_path_greedy(grid)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    larger_grid = make_larger_grid(grid, 5)
    return find_safest_path_greedy(larger_grid)


e.run_tests(2, part2)
e.run_main(2, part2)
