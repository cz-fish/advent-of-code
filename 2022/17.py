#!/usr/bin/python3.8

from aoc import Env

e = Env(17)
e.T(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>", 3068, 1514285714288)


shapes = [
    [
        '####',
    ],
    [
        '.#.',
        '###',
        '.#.',
    ],
    [
        # upside down, going from bottom up
        '###',
        '..#',
        '..#',
    ],
    [
        '#',
        '#',
        '#',
        '#',
    ],
    [
        '##',
        '##',
    ]
]

CHAMBER_WIDTH = 7

def whole_shape_check(stone, left, bottom, height, width, chamber):
    for y in range(height):
        if bottom + y >= len(chamber):
            continue
        for x in range(width):
            if stone[y][x] == '#' and chamber[bottom + y][left + x] == '#':
                return False
    return True


def push_sideways(stone, push, left, bottom, height, width, chamber):
    new_left = left + push
    if new_left < 0 or new_left + width - 1 >= CHAMBER_WIDTH:
        # hit walls
        return left
    if whole_shape_check(stone, new_left, bottom, height, width, chamber):
        return new_left
    return left


def push_down(stone, left, bottom, height, width, chamber):
    if bottom == 0:
        # dropped to the floor
        return bottom, True
    new_bottom = bottom - 1
    if new_bottom >= len(chamber):
        # above the highest rock in the chamber
        return new_bottom, False
    if whole_shape_check(stone, left, new_bottom, height, width, chamber):
        return new_bottom, False
    return bottom, True


def stop_stone(stone, left, bottom, height, width, chamber):
    top = bottom + height
    while len(chamber) < top:
        chamber.append(['.' for _ in range(CHAMBER_WIDTH)])
    for x in range(width):
        for y in range(height):
            if stone[y][x] == '#':
                chamber[bottom + y][left + x] = '#'


def print_chamber(chamber):
    for y in range(len(chamber) - 1, -1, -1):
        print(f'|{"".join(chamber[y])}|')
    print(f'+{"-" * CHAMBER_WIDTH}+')


def drop_stones(jets, number):
    chamber = []
    jet_index = 0
    for i in range(number):
        stone = shapes[i % len(shapes)]
        # new stone appears 2 untis from the left edge and 3 above highest rock
        left = 2
        bottom = len(chamber) + 3
        height = len(stone)
        width = len(stone[0])
        
        while True:
            push = 1 if jets[jet_index] == '>' else -1
            jet_index = (jet_index + 1) % len(jets)
            left = push_sideways(stone, push, left, bottom, height, width, chamber)
            bottom, stop = push_down(stone, left, bottom, height, width, chamber)
            if stop:
                stop_stone(stone, left, bottom, height, width, chamber)
                break

#        if i < 10:
#            print_chamber(chamber)
#            print()

    return chamber


def part1(input):
    jets = input.get_valid_lines()[0]
    chamber = drop_stones(jets, 2022)
    return len(chamber)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    n = 1000000000000
    jets = input.get_valid_lines()[0]
    # input length: 10091 (prime)
    print(len(jets))
    pass


e.run_tests(2, part2)
e.run_main(2, part2)
