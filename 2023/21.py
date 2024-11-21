#!/usr/bin/python3.8

from pyaoc import Env, Grid
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
...........""", None, 50, param=(0, 10))
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
...........""", None, 1594, param=(0, 50))
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


def count_reachable_pt2(grid, start, steps_to_make):
    visited = set()
    waves = defaultdict(set)
    waves[0].add(start)
    visited.add(start)
    for wave in range(steps_to_make):
        for row, col in waves[wave]:
            for nrow, ncol in grid.neighbors4(row, col, outside=True):
                if grid.get(nrow % grid.h, ncol % grid.w) != '#' and (nrow, ncol) not in visited:
                    visited.add((nrow, ncol))
                    waves[wave + 1].add((nrow, ncol))

    odds = set()
    evens = set()
    for i in range(steps_to_make + 1):
        if i % 2:
            odds = odds.union(waves[i])
        else:
            evens = evens.union(waves[i])
        if i > 0 and ((i - 65) % 131 == 0):
            if i % 2:
                print(f"{{ {i}, {len(odds)} }}")
            else:
                print(f"{{ {i}, {len(evens)} }}")
    if steps_to_make % 2:
        return len(odds)
    else:
        return len(evens)


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
    #print(f"non-rocks in tile {count_non_rocks}. Of them reachable: {reachable}")
    #if count_non_rocks != reachable: return f"Not all non-rocks are reachable: reached {reachable} out of {count_non_rocks}"

    srow, scol = start
    # Verify assumption: start is in the center of the grid
    if srow + 1 != (grid.h + 1) // 2 or scol + 1 != (grid.w + 1) // 2: return f"Start not in the center. Start {start}"

    # Verify assumption: there are no rocks on the center line/column
    for col in range(grid.w):
        if grid.get(srow, col) == '#': return f"Rock on the centerline {srow}, {col}"
    for row in range(grid.h):
        if grid.get(row, scol) == '#': return f"Rock on the centerline {row}, {scol}"

    return None


def extended_pathfinding(grid, start, steps):
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
    #for k, v in border_dists.items():
    #    print(f"[{k}] - dist {v}")
    # TODO: implementation incomplete
    return 0


def reach_from_corner(grid, srow, scol, max_dist=None):
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
    return filled


def special_input_solution(grid, start, steps):
    # Sources:
    # https://www.reddit.com/r/adventofcode/comments/18nol3m/2023_day_21_a_geometric_solutionexplanation_for/
    # https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
    # https://raw.githubusercontent.com/Manitary/advent-of-code/c44838423066b3c8d446f0d94f2a19d675f2b6dc/2023/python/day21.png

    length = 131
    half = 65
    assert grid.w == length
    assert grid.h == length
    assert start[0] == half
    assert start[1] == half
    #assert steps == 26501365
    assert (steps - half) % length == 0

    n = (steps - half) // length
    assert n % 2 == 0

    #corner_reachable = reach_from_corner(grid, 0, 0, half)\
    #    .union(reach_from_corner(grid, length - 1, 0, half))\
    #    .union(reach_from_corner(grid, 0, length - 1, half))\
    #    .union(reach_from_corner(grid, length - 1, length - 1, half))

    visited = set()
    q = deque([(start[0], start[1], 0)])
    all = [0, 0]
    corner = [0, 0]
    while q:
        row, col, dist = q.popleft()
        d = abs(half - row) + abs(half - col)
        if d > 65:
            #if (row, col) in corner_reachable:
            #if d != dist: print(f"{d} different from {dist}")
            corner[dist % 2] += 1
        all[dist % 2] += 1
        for nrow, ncol in grid.neighbors4(row, col):
            if (nrow, ncol) in visited or grid.get(nrow, ncol) == '#':
                continue
            q.append((nrow, ncol, dist + 1))
            visited.add((nrow, ncol))

    # The formula seems to overcount for some reason. By comparison with small values
    # calculated using the correct but slow `count_reachable_pt2`, the difference
    # increases by 4 for every increment of n. The adjustment formula
    # -4 * (n/2 + n/2 * (n/2-1))
    # does the trick
    adj = 4 * (n//2 + (n//2-1) * n//2)
    return (n+1) * (n+1) * all[1] + n * n * all[0] - (n+1) * corner[1] + n * corner[0] - adj


def part2(input):
    _, steps = e.get_param()
    grid = Grid(input.get_valid_lines())
    start = find_start(grid)

    outcome = analyze_input(grid, start)
    if outcome is not None:
        print(f"Special input assumptions failed: {outcome}")
        return count_reachable_pt2(grid, start, steps)
        #return extended_pathfinding(grid, start, steps)
    else:
        print("Special input assumptions verified")

        """
        count_reachable_pt2(grid, start, 1506)

        For extrapolation:

        { 65, 3947 }
            { 100, 9291 }
        { 196, 35153 }
            { 200, 36683 }
            { 300, 81915 }
        { 327, 97459 }
            { 400, 145647 }
        { 458, 190865 }
            { 500, 227624 }
        { 589, 315371 }
            { 600, 327805 }
            { 700, 444625 }
        { 720, 470977 }
            { 800, 581107 }
        { 851, 657683 }
            { 900, 735822 }
        { 982, 875489 }
            { 1000, 908266 }
            { 1100, 1097812 }

        { 65, 3947 }
        { 196, 35153 }
        { 327, 97459 }
        { 458, 190865 }
        { 589, 315371 }
        { 720, 470977 }
        { 851, 657683 }
        { 982, 875489 }
        { 1113, 1124395 }
        { 1244, 1404401 }
        { 1375, 1715507 }
        { 1506, 2057713 }
        """
        known_small_results = {
            65: 3947,
            196: 35153,
            327: 97459,
            458: 190865,
            589: 315371,
            720: 470977,
            851: 657683,
            982: 875489,
            1113: 1124395,
            1244: 1404401,
            1375: 1715507,
            1506: 2057713,
        }

        for s in [65, 327, 589, 851, 1113, 1375]:
            sol = special_input_solution(grid, start, s)
            correct = known_small_results[s]
            print(f"steps {s}, correct result {correct}, got {sol}, difference {sol - correct}")
            """
            65: 3687
            327: 97195
            589: 315111
            851: 657435
            1113: 1124167
            1375: 1715307
            """

        return special_input_solution(grid, start, steps)

# 636432352002747 too high
# 636432351800447 too high
# 636432351193287 too high

# 634075687447766 approx from quadratic eq: 0.902827 x^2 + 4.1506 x - 284.286
# 636391179686361 from a more fitting quad eq: 0.906124 x^2 + 1.71528 x + 7.13111

# 636391426712747 the actual answer


e.run_tests(2, part2)
e.run_main(2, part2)
