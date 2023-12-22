#!/usr/bin/python3.8

from aoc import Env, Grid
from collections import deque, defaultdict

def eT(*args,**kvargs):
    pass

e = Env(21, param=(64, 26501365))
e.T("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 16, 16, param=(6, 6))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 50, param=(0, 10))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 1594, param=(0, 50))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 6536, param=(0, 100))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 167004, param=(0, 500))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 668697, param=(0, 1000))
eT("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", None, 16733044, param=(0, 5000))


def find_start(grid):
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.get(row, col) == 'S':
                return row, col
    assert False, "No start found in grid"


def count_reachable(grid, start, steps_to_make):
    visited = set()
    waves = defaultdict(set)
    waves[0].add(start)
    visited.add(start)
    for wave in range(steps_to_make):
        for row, col in waves[wave]:
            for nrow, ncol in grid.neighbors4(row, col):
                if grid.get(nrow, ncol) != '#' and (nrow, ncol) not in visited:
                    visited.add((nrow, ncol))
                    waves[wave + 1].add((nrow, ncol))
    off = steps_to_make % 2
    total = set()
    for i in range(off, steps_to_make + 1, 2):
        total = total.union(waves[i])
    return len(total)



def part1(input):
    steps, _ = e.get_param()
    grid = Grid(input.get_valid_lines())
    start = find_start(grid)
    return count_reachable(grid, start, steps)


e.run_tests(1, part1)
e.run_main(1, part1)


def flood_fill(grid, srow, scol, max_dist=None):
    filled = set()
    filled.add((srow, scol))
    q = deque([(srow, scol, 0)])
    while q:
        row, col, dist = q.popleft()
        if max_dist is not None and dist > max_dist:
            break
        for nrow, ncol in grid.neighbors4(row, col):
            coords = (nrow, ncol)
            if grid.get(nrow, ncol) != '#' and  coords not in filled:
                filled.add(coords)
                q.append((nrow, ncol, dist + 1))
    return len(filled), dist


def find_shortest_distances_to_all_borders(grid, srow, scol):
    visited = set()
    visited.add((srow, scol))
    q = deque([(srow, scol, 0)])
    border = {}
    while q:
        row, col, dist = q.popleft()
        if row == 0 or col == 0 or row == grid.h-1 or col == grid.w-1:
            border[(row, col)] = dist
        for nrow, ncol in grid.neighbors4(row, col):
            coords = (nrow, ncol)
            if grid.get(nrow, ncol) != '#' and  coords not in visited:
                visited.add(coords)
                q.append((nrow, ncol, dist + 1))
    return border


def analyze_input(grid, start):
    # Verify assumption: all border tiles are free
    for row in range(grid.h):
        if grid.get(row, 0) == '#': return f"Rock on border: {row}, 0"
        if grid.get(row, grid.w-1) == '#': return f"Rock on border: {row}, {grid.w-1}"
    for col in range(grid.w):
        if grid.get(0, col) == '#': return f"Rock on border: 0, {col}"
        if grid.get(grid.h-1, col) == '#': return f"Rock on border: {grid.h-1}, {col}"

    # Verify assumption: both dimensions are even
    # [wrong] - they are both odd
    #if grid.w % 2 != 0: return f"Odd width {grid.w}"
    #if grid.h % 2 != 0: return f"Odd height {grid.h}"

    # Assumption: half of the positions are only reachable with odd number of steps and the
    # other half only with even number of steps.
    # But because the grid dimensions are both odd, the set of even-reachable and odd-reachable
    # tiles alternates with each grid repetition in either direction

    # Verify assumption: all non-rocks are reachable
    # [wrong] - not all non-rocks are reachable
    count_non_rocks = 0
    for row in range(grid.h):
        for col in range(grid.w):
            if grid.get(row, col) != '#':
                count_non_rocks += 1
    reachable, _ = flood_fill(grid, 0, 0)
    print(f"non-rocks in tile {count_non_rocks}. Of them reachable: {reachable}")
    #if count_non_rocks != reachable: return f"Not all non-rocks are reachable: reached {reachable} out of {count_non_rocks}"
    
    srow, scol = start
    # Verify assumption: start is in the center of the grid
    # [wrong] - the start is actually 1 position off-center
    #if srow != (grid.h + 1) // 2 or scol != (grid.w + 1) // 2: return f"Start not in the center. Start {start}"

    # Verify assumption: there are no rocks on the center line/column
    for col in range(grid.w):
        if grid.get(srow, col) == '#': return f"Rock on the centerline {srow}, {col}"
    for row in range(grid.h):
        if grid.get(row, scol) == '#': return f"Rock on the centerline {row}, {scol}"

    return None


def part2(input):
    _, steps = e.get_param()
    grid = Grid(input.get_valid_lines())
    start = find_start(grid)
    #outcome = analyze_input(grid, start)
    #if outcome is not None:
    #    print(f"assumptions failed: {outcome}")
    #else:
    #    print("assumptions verified")
    
    tile_capacity, steps_to_fill_first = flood_fill(grid, start[0], start[1], None)
    #print(f"tile capacity {tile_capacity}, steps to fill first {steps_to_fill_first}")
    #for border_row, border_col in [(0, 0), (start[0], 0), (grid.h-1, 0), (grid.h-1, start[1]), (grid.h-1, grid.w-1), (start[0], grid.w-1), (0, grid.w-1), (0, start[1])]:
    #    x, y = flood_fill(grid, border_row, border_col, None)
    #    print(f"starting from {border_row}, {border_col}: filled {x} in {y} steps")

    # TODO: find shortest distances from start to all the edges
    # find shortest distance from an edge to the other edge
    # divide the total number of steps to find out how many tiles we can cross in each direction
    # it takes N steps to fill in a tile, where N <= 2 * a dimension of the tile. So all tiles in each
    # direction up till the second to last will be full.
    # In each tile, only half of the positions are reachable in even number of steps, so the total fill is
    # number_of_tiles * one_tile_fill / 2.
    # Then deal with the last 2 tiles in each direction.
    border_dists = find_shortest_distances_to_all_borders(grid, start[0], start[1])
    for k, v in border_dists.items():
        print(f"[{k}] - dist {v}")

    return 0


e.run_tests(2, part2)
e.run_main(2, part2)
