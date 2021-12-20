#!/usr/bin/python3.8

from aoc import Env, Grid

e = Env(20)
e.T("""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""", 35, 3351)


def load_input(input, buffer):
    gr = input.get_groups()
    assert len(gr) == 2
    pixelmap = gr[0][0]
    assert len(pixelmap) == 512, f"pixelmap length = {len(pixelmap)}"

    w = len(gr[1][0])
    w += 2 * buffer
    grid = ['.' * w for _ in range(buffer)]
    for ln in gr[1]:
        grid.append(('.' * buffer) + ln + ('.') * buffer)
    for i in range(buffer):
        grid.append('.' * w)
    return pixelmap, Grid(grid)


def apply_filter(pixelmap, grid, fill):
    n = [
        ['.' for _ in range(grid.w)]
        for _ in range(grid.h)
    ]
    def get(y, x):
        if not grid.is_in(y, x):
            return fill
        else:
            return grid.get(y, x)
    for y in range(grid.h):
        for x in range(grid.w):
            mask = get(y-1, x-1) + get(y-1, x) + get(y-1, x+1) + \
                   get(y, x-1) + get(y, x) + get(y, x+1) + \
                   get(y+1, x-1) + get(y+1, x) + get(y+1, x+1)
            index = int(''.join([{'.':'0', '#':'1'}[c] for c in mask]), 2)
            rep = pixelmap[index]
            n[y][x] = rep
    grid.grid = n


def count_light(grid):
    count = 0
    for ln in grid.grid:
        count += sum(1 for x in ln if x == '#')
    return count


def print_grid(grid):
    print('------')
    for ln in grid.grid:
        print(''.join(ln))
    print('------')


def part1(input):
    pixelmap, grid = load_input(input, 2)

    fill_first = '.'
    fill_even = pixelmap[0]
    fill_odd = fill_even if fill_even == '.' else pixelmap[-1]

    apply_filter(pixelmap, grid, fill_first)
    apply_filter(pixelmap, grid, fill_even)
    return count_light(grid)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pixelmap, grid = load_input(input, 50)

    fill_first = '.'
    fill_even = pixelmap[0]
    fill_odd = fill_even if fill_even == '.' else pixelmap[-1]

    fill = fill_first
    for i in range(50):
        apply_filter(pixelmap, grid, fill)
        fill = fill_even if i % 2 == 0 else fill_odd
    return count_light(grid)


e.run_tests(2, part2)
e.run_main(2, part2)
