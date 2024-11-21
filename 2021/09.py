#!/usr/bin/python3.8

from pyaoc import Env, Grid

e = Env(9)
e.T("""2199943210
3987894921
9856789892
8767896789
9899965678""", 15, 1134)


def part1(input):
    grid = Grid(input.get_valid_lines())
    risk_level = 0
    for row in range(grid.h):
        for col in range(grid.w):
            val = int(grid.get(row, col))
            for n in [int(grid.get(r, c)) for (r,c) in grid.neighbors4(row, col)]:
                if n <= val:
                    break
            else:
                risk_level += val + 1
    return risk_level


e.run_tests(1, part1)
e.run_main(1, part1)


def mark_basin(grid, row, col):
    st = [(row, col)]
    st_pos = 0
    size = 0
    while st_pos < len(st):
        r, c = st[st_pos]
        st_pos += 1
        if grid.get(r, c) != '9':
            grid.grid[r][c] = '9'
            size += 1
            st += grid.neighbors4(r, c)
    return size


def part2(input):
    grid = Grid(input.get_valid_lines())
    top3_basins = []
    for row in range(grid.h):
        for col in range(grid.w):
            val = grid.get(row, col)
            if val != '9':
                size = mark_basin(grid, row, col)
                if len(top3_basins) < 3:
                    top3_basins.append(size)
                elif top3_basins[0] < size:
                    top3_basins = top3_basins[1:] + [size]
                top3_basins.sort()
    assert len(top3_basins) == 3
    return top3_basins[0] * top3_basins[1] * top3_basins[2]


e.run_tests(2, part2)
e.run_main(2, part2)
