#!/usr/bin/python3.12

from pyaoc import Env

e = Env(12)
e.T("""0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2""", 2, None)


def parse_input(input):
    g = input.get_groups()
    # tile groups. Assuming each tile fits in 3x3 square
    tiles = []
    for i in range(0, len(g)-1):
        tgroup = g[i]
        assert len(tgroup) == 4
        tile = tgroup[1:]
        assert all(len(x) == 3 for x in tile)
        tiles.append(tile)
    # problems - the last group
    problems = []
    for ln in g[-1]:
        left, right = ln.split(': ')
        w, h = (int(x) for x in left.split('x'))
        counts = [int(x) for x in right.split(' ')]
        problems.append((w, h, counts))
    return tiles, problems


def get_tile_size(tile):
    return sum(1 for x in ''.join(tile) if x == '#')


def part1(input):
    tiles, problems = parse_input(input)
    print(f"Num problems: {len(problems)}")
    tile_sizes = {i: get_tile_size(tiles[i]) for i in range(len(tiles))}
    size_ok = 0
    for w, h, counts in problems:
        space_needed = sum([counts[i] * tile_sizes[i] for i in range(len(counts))])
        space_available = w * h
        if space_needed <= space_available:
            size_ok += 1
    return size_ok


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
