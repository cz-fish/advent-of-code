#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict

e = Env(24)
e.T("""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""", 10, 2208)


move = {
    'se': (1, 1),
    'sw': (1, -1),
    'w': (0, -2),
    'nw': (-1, -1),
    'ne': (-1, 1),
    'e': (0, 2)
}


def find_tile(tile):
    row = 0
    col = 0
    idx = 0
    while idx < len(tile):
        if tile[idx] in 'sn':
            d = tile[idx:idx+2]
            idx += 2
        else:
            d = tile[idx]
            idx += 1
        assert d in move
        m = move[d]
        row += m[0]
        col += m[1]
    return row, col


def get_blacks(paint):
    return [c for c, p in paint.items() if p]


def part1(input):
    tiles = input.get_valid_lines()
    paint = defaultdict(bool)
    for tile in tiles:
        row, col = find_tile(tile)
        paint[(row, col)] = not paint[(row, col)]
    return len(get_blacks(paint))


e.run_tests(1, part1)
e.run_main(1, part1)


def life_step(blacks, paint):
    consider = set(blacks)
    for row, col in blacks:
        for a, b in move.values():
            consider.add((row + a, col + b))
    repaint = {}
    for row, col in consider:
        neighbors = 0
        for a, b in move.values():
            if paint[(row + a, col + b)]:
                neighbors += 1
        current = paint[(row, col)]
        if current == True and (neighbors == 0 or neighbors > 2):
            repaint[(row, col)] = False
        elif current == False and neighbors == 2:
            repaint[(row, col)] = True

    for coord, val in repaint.items():
        paint[coord] = val


def part2(input):
    tiles = input.get_valid_lines()
    paint = defaultdict(bool)
    for tile in tiles:
        row, col = find_tile(tile)
        paint[(row, col)] = not paint[(row, col)]
    blacks = get_blacks(paint)
    for step in range(100):
        life_step(blacks, paint)
        blacks = get_blacks(paint)
    return len(blacks)


e.run_tests(2, part2)
e.run_main(2, part2)
