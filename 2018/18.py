#!/usr/bin/python3.8

from pyaoc import Env, Grid

e = Env(18)
e.T(""".#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""", 37*31, 0)


def evolve(old_grid):
    grid = Grid.copygrid(old_grid)
    for row in range(old_grid.h):
        for col in range(old_grid.w):
            trees = 0
            lumber = 0
            for pos in old_grid.neighbors8(row, col):
                c = old_grid.get(pos[0], pos[1])
                if c == '|':
                    trees += 1
                elif c == '#':
                    lumber += 1
            c = old_grid.get(row, col)
            if c == '.' and trees >= 3:
                # Open pos with 3 or more trees becomes trees
                grid.grid[row][col] = '|'
            elif c == '|' and lumber >= 3:
                # Trees with 3 or more lumber becomes lumber
                grid.grid[row][col] = '#'
            elif c == '#' and (lumber < 1 or trees < 1):
                # Lumber remains lumber only if next to
                # at least 1 other lumber and 1 trees
                grid.grid[row][col] = '.'
    return grid


def count(grid):
    wood = 0
    lumber = 0
    for row in range(grid.h):
        wood += sum([1 for x in grid.grid[row] if x == '|'])
        lumber += sum([1 for x in grid.grid[row] if x == '#'])
    return wood * lumber


def print_world(grid):
    for row in range(grid.h):
        print(''.join(grid.grid[row]))
    print("-------------------")


def part1(input):
    N = 10
    grid = Grid(input.get_valid_lines())
    #print_world(grid)
    for step in range(N):
        grid = evolve(grid)
        # uncomment for a cool plasma effect
        #print_world(grid)
    return count(grid)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    N = 1000000000
    grid = Grid(input.get_valid_lines())

    serialize = lambda g: ''.join([''.join(r) for r in grid.grid])

    configs = {}
    values = {}
    generation = 0
    configs[serialize(grid)] = generation
    values[generation] = count(grid)
    while generation < N:
        if generation > 0 and generation % 100 == 0:
            print(f"generation={generation}")
        generation += 1
        grid = evolve(grid)
        s = serialize(grid)
        if s in configs:
            prev_gen = configs[s]
            cycle_len = generation - prev_gen
            remaining_gens = N - generation
            same_setup = prev_gen + remaining_gens % cycle_len
            print(f"""Generation {generation} is the same as generation {prev_gen}.
Period {cycle_len}; {remaining_gens} remaining to target generation {N}
N will be {remaining_gens % cycle_len}-th generation of the cycle. That is the same as generation {same_setup}""")
            return values[same_setup]
        configs[s] = generation
        values[generation] = count(grid)
    else:
        # This should not be reached
        print("You've waited this long?!")
        return count(grid)


e.run_tests(2, part2)
e.run_main(2, part2)
