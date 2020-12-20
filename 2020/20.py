#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict
from functools import reduce
import math
import re

e = Env(20)
e.T("""Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...


""", 20899048083289, 273)

monster = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


def get_tiles(input):
    gr = input.get_groups()
    tiles = {}
    for tile in gr:
        if not tile:
            continue
        m = re.match(r'^Tile (\d+):', tile[0])
        assert m is not None
        number = int(m.group(1))
        grid = tile[1:]
        tiles[number] = grid
    return tiles


def get_edges(tiles):
    all_edges = defaultdict(list)
    tile_edges = {}
    for number, tile in tiles.items():
        all_edges[tile[0]] += [number]
        all_edges[tile[0][::-1]] += [number]
        all_edges[tile[-1]] += [number]
        all_edges[tile[-1][::-1]] += [number]
        left = ''.join([r[0] for r in tile[::-1]])
        all_edges[left] += [number]
        all_edges[left[::-1]] += [number]
        right = ''.join([r[-1] for r in tile])
        all_edges[right] += [number]
        all_edges[right[::-1]] += [number]

        """ clockwise
            --->
            ^  |
            |  v
            <--- """
        tile_edges[number] = [tile[0][:], right, tile[-1][::-1], left]
    return all_edges, tile_edges


def tile_border_edges(tile_nr, all_edges, tile_edges):
    border_edges = []
    for i, e in enumerate(tile_edges[tile_nr]):
        if len(all_edges[e]) == 1:
            border_edges += [(e, i)]
    return border_edges


def find_corners_from_edges(tiles, all_edges, tile_edges):
    corner_tiles = []
    # edge_tiles = []
    for number, _ in tiles.items():
        border_edges = tile_border_edges(number, all_edges, tile_edges)
        if len(border_edges) == 1:
            # edge_tiles += [number]
            pass
        elif len(border_edges) == 2:
            corner_tiles += [number]
        else:
            assert len(border_edges) == 0

    # print(f"corner tiles {corner_tiles}")
    # print(edge_tiles)
    assert len(corner_tiles) == 4, f"Found {len(corner_tiles)} corners instead of 4!"
    return corner_tiles


def find_corners(input):
    tiles = get_tiles(input)
    all_edges, tile_edges = get_edges(tiles)

    shared_edge_counts = [len(i) for i in all_edges.values()]
    assert max(shared_edge_counts) == 2, "There are multiple different matchings on the same edge"

    # for k, v in edges.items():
    #     print(f"{k}: {v}")
    return find_corners_from_edges(tiles, all_edges, tile_edges)


def part1(input):
    corner_tiles = find_corners(input)
    return reduce(lambda a, b: a * b, corner_tiles)


e.run_tests(1, part1)
e.run_main(1, part1)


def flip_and_rotate(image):
    for _ in range(2):
        # rotate
        image = [[image[c][r] for c in range(len(image[0]))] for r in range(len(image))]
        for _ in range(2):
            # flip horizontally
            image = [r[::-1] for r in image]
            for _ in range(2):
                # flip_vertically
                image = image[::-1]
                yield image


def place_tile(tiles, tile_nr, coords, grid, match_edges):
    assert match_edges[0][-1] == match_edges[1][0]
    row, col = coords
    tile = tiles[tile_nr]
    # flip and rotate until the edges are matched
    for orient in flip_and_rotate(tile):
        left = ''.join([r[0] for r in orient[::-1]])
        top = ''.join(orient[0])
        if left == match_edges[0] and top == match_edges[1]:
            # this is the right orientation
            placement = grid[row][col]
            placement['number'] = tile_nr
            placement['tile'] = orient
            right = ''.join([r[-1] for r in orient[::-1]])
            bottom = ''.join(orient[-1])
            placement['right'] = right
            placement['bottom'] = bottom
            return True

    return False
    # assert False, f"Cannot orient tile {tile_nr} to match edges: {match_edges}"


def complete_match(borders, tile_nr, all_edges, tile_edges):
    # borders is either [None, <top edge>] or [<left edge>, None]
    # tile `tile_nr` has to have one or two loose edges, and one of them
    # must be adjacent to either the <top edge> or the <left edge>

    # this needs to be an edge tile - with one edge on the border
    # but it can also be an unused corner with 2 edges on the border
    edge = tile_border_edges(tile_nr, all_edges, tile_edges)
    assert len(edge) >= 1
    other_edge = [e for e in borders if e][0]
    rev_edge = other_edge[::-1]
    for i, e in enumerate(tile_edges[tile_nr]):
        if e == other_edge:
            prev = tile_edges[tile_nr][(i-1)%4]
            next = tile_edges[tile_nr][(i+1)%4]
            break
        elif e == rev_edge:
            prev = tile_edges[tile_nr][(i+1)%4][::-1]
            next = tile_edges[tile_nr][(i-1)%4][::-1]
            break
    else:
        assert False, f"Cannot complete edge match for tile_nr {tile_nr}, borders: {borders}"
    if borders[0] == None:
        return [prev, other_edge]
    else:
        return [other_edge, next]


def print_part_grid(grid, verbose):
    for row in grid:
        for col in row:
            if 'number' in col:
                print(f"{col['number']} ", end='')
        print('')
    print('-------')
    if verbose:
        for row in grid:
            for i in range(10):
                for col in row:
                    if 'tile' not in col:
                        continue
                    print(''.join(col['tile'][i]) + ' ', end='')
                print('')
            print('')


def remove_borders(tile_grid):
    tile_h = len(tile_grid[0][0]['tile'])
    grid = []
    for row in tile_grid:
        for i in range(1, tile_h - 1):
            grid += ['']
            for col in row:
                tile = col['tile']
                grid[-1] += ''.join(tile[i][1:-1])
    return grid


def put_tiles_together(tiles, all_edges, tile_edges, corner_tiles):
    size = int(math.sqrt(len(tiles)))
    assert size * size == len(tiles)
    print(f"{len(tiles)} tiles, Image: {size} x {size} tiles")
    grid = [[{} for i in range(size)] for j in range(size)]

    already_placed = set()

    # fill the whole grid
    for col in range(size):
        for row in range(size):
            # print(f"tile {row}/{col}")
            opts = set()
            if col == 0 and row == 0:
                # pick a corner
                opts.add(corner_tiles[0])
                # find the two border edges - one will be at the top and one on the left
                borders = tile_border_edges(corner_tiles[0], all_edges, tile_edges)
                assert len(borders) == 2
                # but make sure that they are in the right order
                if borders[0][1] == (borders[1][1] + 1) % 4:
                    borders = [borders[1][0], borders[0][0]]
                else:
                    borders = [borders[0][0], borders[1][0]]
            elif col == 0:
                borders = [None, grid[row-1][col]['bottom']]
                opts = set(all_edges[borders[1]])
            elif row == 0:
                borders = [grid[row][col-1]['right'], None]
                opts = set(all_edges[borders[0]])
            else:
                borders = [grid[row][col-1]['right'], grid[row-1][col]['bottom']]
                opts = set(all_edges[borders[0]]) & set(all_edges[borders[1]])
            # print(f"  borders {borders}")
            # print(f"  opts {opts}")
            opts = opts - already_placed
            assert len(opts) == 1, f"cannot choose tile for {row}, {col}: {len(opts)} options"
            tile_nr = list(opts)[0]
            # print(f"  {row}/{col} - placing tile {tile_nr}")

            # now if one of `borders` is None, we have to find out which of the edges
            # of the `tile_nr` is free and in which direction should we use it
            if None in borders:
                borders = complete_match(borders, tile_nr, all_edges, tile_edges)
            # print(f"  borders {borders}")

            # rotate and flip the tile so that it matches the desired top and left edge (borders)
            assert place_tile(tiles, tile_nr, (row, col), grid, borders), f"cannot place tile {tile_nr}"
            already_placed.add(tile_nr)
    print_part_grid(grid, False)
    return grid


def find_monsters(grid):
    grid = [''.join(r) for r in grid]
    hei = len(grid)
    wid = len(grid[0])
    mwid = len(monster[0])
    monsters = []
    for line in range(1, hei-1):
        for i in range(0, wid - mwid + 1):
            if (
                re.match(monster[0], grid[line-1][i:i+mwid]) and
                re.match(monster[1], grid[line][i:i+mwid]) and
                re.match(monster[2], grid[line+1][i:i+mwid])):
                monsters += [(line-1, i)]
    return monsters


def paint_monster(grid, coords, color):
    for r in range(len(monster)):
        for c in range(len(monster[r])):
            x = coords[1] + c
            y = coords[0] + r
            if monster[r][c] == '#':
                assert grid[y][x] == '#', f"Overlapping monsters at {y}, {x}!"
                grid[y][x] = chr(ord('A') + color)


def part2(input):
    tiles = get_tiles(input)
    all_edges, tile_edges = get_edges(tiles)
    corner_tiles = find_corners_from_edges(tiles, all_edges, tile_edges)
    tile_grid = put_tiles_together(tiles, all_edges, tile_edges, corner_tiles)
    grid = remove_borders(tile_grid)

    water = 0
    for orientation, rotated_grid in enumerate(flip_and_rotate(grid)):
        monsters = find_monsters(rotated_grid)
        print(f"orientation {orientation}, monsters: {len(monsters)}, {monsters}")

        if not monsters:
            continue

        # It seems that there is only one orientation that has monsters;
        # all other orientations are monster-free. So if this one has monsters
        # then this is the one.
        for i, coords in enumerate(monsters):
            paint_monster(rotated_grid, coords, i)

        for row in rotated_grid:
            print(''.join(row))

        water = sum([row.count('#') for row in rotated_grid])

    return water


e.run_tests(2, part2)
e.run_main(2, part2)

