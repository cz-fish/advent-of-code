#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict
from functools import reduce
import math
import re
import random

e = Env(20)

monster = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]

frame_counter = 0

frame = []
for r in range(12 * 10):
    frame += [[' ']*12*10]

palette = {
    ' ': '000000',  # blank space
    '.': '99d9ea',  # water - low
    '#': '00a2e8',  # water - high
    '-': 'ff7da8',  # picture border - low
    '@': 'ff3778',  # picture border - high
    ';': '9e9e9e',  # tile edge - low
    '*': '434343',  # tile edge - high
    '$': 'f5bf03',  # high water highlighted
}

random.seed(1237)

for i in range(26):
    palette[chr(ord('A') + i)] = 'ff0000'
    """
    v = [
        random.randint(0, 127) + 128,
        random.randint(0, 127),
        random.randint(0, 127)
    ]
    random.shuffle(v)
    palette[chr(ord('A') + i)] = f'{v[0]:02x}{v[1]:02x}{v[2]:02x}'
    """


def frame_write():
    global frame_counter
    scale = 8
    wid = 12 * 10 * scale
    hei = 12 * 10 * scale
    with open(f'{frame_counter:03}.xpm', 'wt') as f:
        print("! XPM2", file=f)
        print(f"{wid} {hei} {len(palette)} 1", file=f)
        for k, col in palette.items():
            print(f"{k} c #{col}", file=f)
        for line in frame:
            for j in range(scale):
                print(''.join([c * scale for c in line]), file=f)
    frame_counter += 1


def frame_blit(left, top, grid):
    global frame
    h = len(grid)
    w = len(grid[0])
    for x in range(w):
        for y in range(h):
            frame[y + top][x + left] = grid[y][x]


def frame_clear(left, top, width, height):
    block = []
    for r in range(height):
        block += [[' '] * width]
    frame_blit(left, top, block)


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


def remove_borders(tile_grid, coords, xtiles):
    frame_clear(0, 0, 12*10, 12*10)
    tile_h = len(tile_grid[0][0]['tile'])
    grid = []
    for row in tile_grid:
        for i in range(1, tile_h - 1):
            grid += ['']
            for col in row:
                tile = col['tile']
                grid[-1] += ''.join(tile[i][1:-1])
    for row in range(12):
        for col in range(12):
            for nr, crd in coords.items():
                if crd[0] == row and crd[1] == col:
                    tile_nr = nr
                    break
            bigtile = xtiles[tile_nr]
            block = []
            for j in range(1, 9):
                block += [bigtile[j][1:9]]
            frame_blit(col * 10 + 1, row * 10 + 1, block)
            xtiles[tile_nr] = block
    frame_write()
    frame_write()
    frame_write()
    frame_write()
    
    frame_clear(0, 0, 12*10, 12*10)

    offset = 12
    for row in range(12):
        for col in range(12):
            for nr, crd in coords.items():
                if crd[0] == row and crd[1] == col:
                    tile_nr = nr
                    break
            frame_blit(offset + col * 8, offset + row * 8, xtiles[tile_nr])
    frame_write()
    frame_write()
    frame_write()
    frame_write()

    return grid


def paint_corner(row, col, tile):
    xtile = []
    for j in range(10):
        if col == 11:
            rightcol = '-@'
        else:
            rightcol = ';*'
        if col == 0:
            leftcol = '-@'
        else:
            leftcol = ';*'
        if j in [0, 9]:
            if (j == 0 and row == 0) or (j == 9 and row == 11):
                colormap = '-@'
            else:
                colormap = ';*'
            xtile += [[pmap(x, colormap) for x in tile[j]]]
        else:
            xtile += [[pmap(tile[j][0], leftcol)] + [c for c in tile[j][1:9]] + [pmap(tile[j][9], rightcol)]]
    return xtile


def put_tiles_together(tiles, all_edges, tile_edges, corner_tiles, coords, xtiles):
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

            # swap
            oldswap = 0
            for nr, crd in coords.items():
                if crd[0] == row and crd[1] == col:
                    oldswap = nr
                    break
            newswap = tile_nr
            prev_coords = coords[newswap]
            assert prev_coords[1] > col or (prev_coords[1] == col and prev_coords[0] >= row), f"{(row, col)}, {prev_coords}"
            frame_blit(prev_coords[1] * 10, prev_coords[0] * 10, xtiles[oldswap])
            xtile = paint_corner(row, col, grid[row][col]['tile'])
            frame_blit(col * 10, row * 10, xtile)
            frame_write()
            # update maps after swap
            coords[oldswap] = (prev_coords[0], prev_coords[1])
            coords[newswap] = (row, col)
            xtiles[newswap] = xtile

    # print_part_grid(grid, False)
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


def pmap(bit, subst):
    if bit == '.':
        return subst[0]
    elif bit == '#':
        return subst[1]
    else:
        return bit


def part2(input):
    global frame_counter

    tiles = get_tiles(input)
    xtiles = {}

    coords = {}
    i = 0
    for tile_nr, tile in tiles.items():
        row = i % 12
        col = i // 12
        coords[tile_nr] = (row, col)
        xtile = []
        for j in range(10):
            if j in [0, 9]:
                xtile += [[pmap(x, ';*') for x in tile[j]]]
            else:
                xtile += [[pmap(tile[j][0], ';*')] + [c for c in tile[j][1:9]] + [pmap(tile[j][9], ';*')]]
        frame_blit(col * 10, row * 10, xtile)
        i += 1
        xtiles[tile_nr] = xtile
    frame_write()

    all_edges, tile_edges = get_edges(tiles)

    for tile_nr, tile in tiles.items():
        border = tile_border_edges(tile_nr, all_edges, tile_edges)
        if not border:
            continue
        bv = [b[1] for b in border]
        row, col = coords[tile_nr]
        xtile = []
        for j in range(10):
            if 1 in bv:
                rightcol = '-@'
            else:
                rightcol = ';*'
            if 3 in bv:
                leftcol = '-@'
            else:
                leftcol = ';*'
            if j in [0, 9]:
                if (j == 0 and 0 in bv) or (j == 9 and 2 in bv):
                    colormap = '-@'
                else:
                    colormap = ';*'
                xtile += [[pmap(x, colormap) for x in tile[j]]]
            else:
                xtile += [[pmap(tile[j][0], leftcol)] + [c for c in tile[j][1:9]] + [pmap(tile[j][9], rightcol)]]
        frame_blit(col * 10, row * 10, xtile)
        xtiles[tile_nr] = xtile
    frame_write()

    corner_tiles = find_corners_from_edges(tiles, all_edges, tile_edges)
    tile_grid = put_tiles_together(tiles, all_edges, tile_edges, corner_tiles, coords, xtiles)
    grid = remove_borders(tile_grid, coords, xtiles)

    water = 0
    for orientation, rotated_grid in enumerate(flip_and_rotate(grid)):
        frame_blit(12, 12, rotated_grid)
        frame_write()
        frame_write()
        frame_write()
        frame_write()

        monsters = find_monsters(rotated_grid)
        # print(f"orientation {orientation}, monsters: {len(monsters)}, {monsters}")

        if not monsters:
            continue

        # It seems that there is only one orientation that has monsters;
        # all other orientations are monster-free. So if this one has monsters
        # then this is the one.
        for i, coords in enumerate(monsters):
            paint_monster(rotated_grid, coords, i)
            frame_blit(12, 12, rotated_grid)
            frame_write()
            frame_write()
            frame_write()
            frame_write()

        # for row in rotated_grid:
        #     print(''.join(row))

        water = sum([row.count('#') for row in rotated_grid])

        global frame
        for rep in range(10):
            for i in range(120):
                for j in range(120):
                    if frame[j][i] == '#':
                        frame[j][i] = '$'
                    elif frame[j][i] == '$':
                        frame[j][i] = '#'
            frame_write()
            frame_write()
        break

    return water


e.run_main(2, part2)
