#!/usr/bin/python3.8

from aoc import Env, Grid

e = Env(14)
e.T("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""", 136, 64)


def print_state(rocks, stones, width, height, fname):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    #print(f"width {width} height {height}, rocks: {rocks}, stones: {stones}")
    for col, line in enumerate(rocks):
        for row in line:
            grid[row][col] = '#'
    for col, line in enumerate(stones):
        for row in line:
            grid[row][col] = 'O'

    if fname is None:
        for ln in grid:
            print(''.join(ln))
    else:
        with open(fname, 'wt') as f:
            print(f"""! XPM2
{width} {height} 3 1
. c #444444
O c #308030
# c #ba4444""", file=f)
            for ln in grid:
                print(''.join(ln), file=f)


def classify(line):
    rocks = []
    stones = []
    for i, c in enumerate(line):
        if c == '#':
            rocks.append(i)
        elif c == 'O':
            stones.append(i)
    return rocks, stones

def tilt_one_line(rocks, stones):
    last_pos = -1
    rock_index = 0
    stone_index = 0
    new_stones = []
    for stone in stones:
        while rock_index < len(rocks) and rocks[rock_index] < stone:
            last_pos = rocks[rock_index]
            rock_index += 1
        assert last_pos + 1 <= stone, f"Stone moving backwards, rocks {rocks} stones {stones} last_pos {last_pos} rock_index {rock_index} stone {stone}"
        new_stones.append(last_pos + 1)
        last_pos = last_pos + 1
    return new_stones


def part1(input):
    g = Grid(input.get_valid_lines())
    total = 0
    for c in range(g.w):
        line = ''.join([g.get(r, c) for r in range(g.h)])
        rocks, stones = classify(line)
        moved_stones = tilt_one_line(rocks, stones)
        total += sum([g.h - s for s in moved_stones])
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def classify_grid(g):
    rock_grid = []
    stone_grid = []
    for c in range(g.w):
        line = ''.join([g.get(r, c) for r in range(g.h)])
        r, s = classify(line)
        rock_grid.append(r)
        stone_grid.append(s)
    return rock_grid, stone_grid

#FIXME: not needed
def rotate_90_ccw(lists, height):
    new_lists = [[] for _ in range(height)]
    for c in range(len(lists) - 1, -1, -1):
        for pos in lists[c]:
            new_lists[pos].append(height - 1 - c)
    return new_lists


def rotate_90_cw(lists, height):
    new_lists = [[] for _ in range(height)]
    for c in range(len(lists)):
        for pos in lists[c][::-1]:
            new_lists[height - 1 - pos].append(c)
    return new_lists


def run_cycle(rocks, stones, width, height):
    for d in range(4):
        new_stones = []
        for col in range(width):
            new_stones.append(tilt_one_line(rocks[col], stones[col]))
        stones = new_stones
        #print(f"\nafter tilt {d+1}\n")
        #print_state(rocks, stones, width, height, f"tilt_{d}.xpm")
        # rotate 90 degrees clockwise for the next tilt
        rocks = rotate_90_cw(rocks, height)
        stones = rotate_90_cw(stones, height)
        width, height = height, width
        #print(f"\nafter rotation {d+1}\n")
        #print_state(rocks, stones, width, height, f"rotate_{d}.xpm")
    return stones

def make_key(stones):
    return str(stones)

def part2(input):
    g = Grid(input.get_valid_lines())
    # column-based list of rocks, stones in each column of the grid
    rocks, stones = classify_grid(g)
    #print_state(rocks, stones, g.w, g.h, None)
    configs = {make_key(stones): 0}
    target = 1000000000
    steps = 0
    while steps < target:
        stones = run_cycle(rocks, stones, g.w, g.h)
        #print(f"\nAfter cycle {i+1}\n")
        #print_state(rocks, stones, g.w, g.h, None) 
        key = make_key(stones)
        steps += 1
        if key in configs:
            first = configs[key]
            print(f"config repeats: first {first} now {steps}")
            break
        configs[key] = steps
    period = steps - first
    A = (target - first) % period + first
    assert A >= first
    assert A < steps
    for config, st in configs.items():
        if st == A:
            # config is the final configuration of the board after `target` cycles
            # FIXME: avoid using eval
            final_stones = eval(config)
            break
    else:
        assert False, f"Configuration for state {A} not found in configs"
    
    total = 0
    for col in final_stones:
        total += sum([g.h - s for s in col])
    return total

e.run_tests(2, part2)
e.run_main(2, part2)
