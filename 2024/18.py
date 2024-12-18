#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque

e = Env(18, param=(71, 1024))
e.T("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""", 22, "6,1", param=(7, 12))


def print_grid(g):
    for r in range(g.h):
        ln = ''.join(g.grid[r])
        print(ln)


def shortest_path_length(g):
    q = deque()
    q.append((0, 0, 0))
    visited = set([(0, 0)])
    while q:
        x, y, dist = q.popleft()
        if x == g.w - 1 and y == g.h - 1:
            return dist
        for ny, nx in g.neighbors4(y, x):
            if (nx, ny) in visited:
                continue
            if g.get(ny, nx) == '#':
                continue
            visited.add((nx, ny))
            q.append((nx, ny, dist+1))
    return None


def make_empty_grid(grid_size):
    matrix = [
        ['.' for _ in range(grid_size)]
        for _ in range(grid_size)
    ]
    return Grid(matrix)


def drop_bytes(g, coords):
    for x, y in coords:
        g.grid[y][x] = '#'


def parse_input(input):
    coords = [list(map(int, ln.split(','))) for ln in input.get_valid_lines()]
    grid_size, bytes_drop = e.get_param()
    assert bytes_drop <= len(coords)
    assert [0, 0] not in coords
    return coords, grid_size, bytes_drop


def part1(input):
    coords, grid_size, bytes_drop = parse_input(input)
    g = make_empty_grid(grid_size)
    drop_bytes(g, coords[:bytes_drop])
    #print_grid(g)
    return shortest_path_length(g)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    coords, grid_size, bytes_drop = parse_input(input)
    min_bytes = bytes_drop
    max_bytes = len(coords)
    while max_bytes - min_bytes > 1:
        middle = (min_bytes + max_bytes) // 2
        g = make_empty_grid(grid_size)
        drop_bytes(g, coords[:middle])
        d = shortest_path_length(g)
        #print(min_bytes, max_bytes, middle, d)
        if d is None:
            max_bytes = middle - 1
        else:
            min_bytes = middle
    obstacle = coords[min_bytes+1]
    return f"{obstacle[0]},{obstacle[1]}"


e.run_tests(2, part2)
e.run_main(2, part2)
