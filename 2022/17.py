#!/usr/bin/python3.8

from pyaoc import Env

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


def move_one_stone(jets, jet_index, shape_index, chamber, commit = True):
    stone = shapes[shape_index]
    # new stone appears 2 untis from the left edge and 3 above highest rock
    left = 2
    bottom = len(chamber) + 3
    height = len(stone)
    width = len(stone[0])
    starting_level = bottom

    while True:
        push = 1 if jets[jet_index] == '>' else -1
        jet_index = (jet_index + 1) % len(jets)
        left = push_sideways(stone, push, left, bottom, height, width, chamber)
        bottom, stop = push_down(stone, left, bottom, height, width, chamber)
        if stop:
            if commit:
                stop_stone(stone, left, bottom, height, width, chamber)
            break
    return jet_index, starting_level - bottom


def drop_stones(jets, jet_index, first_stone_index, number, chamber):
    for i in range(number):
        shape_index = (i + first_stone_index) % len(shapes)
        jet_index, _ = move_one_stone(jets, jet_index, shape_index, chamber)
    return chamber, jet_index


def part1(input):
    jets = input.get_valid_lines()[0]
    chamber, _ = drop_stones(jets, 0, 0, 2022, [])
    return len(chamber)


e.run_tests(1, part1)
e.run_main(1, part1)


def find_stone_repetition_start(jets):
    chamber = []
    jet_index = 0
    stone_counter = 0

    simulation = {}
    subsequent_matches = 0

    limit = 2000
    while stone_counter < limit:
        shape_index = stone_counter % len(shapes)
        starting_jet = jet_index
        jet_index, amount_dropped = move_one_stone(jets, jet_index, shape_index, chamber)
        stone_counter += 1

        key = (starting_jet, shape_index, amount_dropped)
        if key in simulation:
            #print(f"configuration {key} last seen at {simulation[key][0]}, now {stone_counter}, height difference {len(chamber)-simulation[key][1]}")
            subsequent_matches += 1
        else:
            subsequent_matches = 0
        simulation[key] = (stone_counter, len(chamber))

        if subsequent_matches == 100:
            repetition_begin = stone_counter - 100
            print(f"Repetition starts after {repetition_begin} stones")
            return repetition_begin

    assert False, f"cannot find repetition after dropping {limit} stones"


def find_stone_period(jets, chamber, start_jet_index, start_shape_index):
    num_period_stones = 0
    jet_index = start_jet_index
    first = None

    while True:
        shape_index = (num_period_stones + start_shape_index) % len(shapes)
        _, amount_dropped = move_one_stone(jets, jet_index, shape_index, chamber, False)

        key = (jet_index, shape_index, amount_dropped)
        if key == first:
            # found repetition
            break
        if first is None:
            first = key

        # commit the stone
        jet_index, _ = move_one_stone(jets, jet_index, shape_index, chamber, True)

        num_period_stones += 1

    return num_period_stones, chamber, jet_index


def part2(input):
    n = 1000000000000
    jets = input.get_valid_lines()[0]

    # find out when do the stones start to repeat
    num_bottom_stones = find_stone_repetition_start(jets)
    # the bottom part is odd, take its height separately
    bottom_chamber, bottom_jet_index = drop_stones(jets, 0, 0, num_bottom_stones, [])
    bottom_shape_index = num_bottom_stones % len(shapes)
    # find the shape and height of 1 period of the repeating stones
    bottom_height = len(bottom_chamber)
    print(f"Bottom part: {num_bottom_stones} stones, {bottom_height} height, {bottom_jet_index} jet index")
    num_period_stones, chamber_after_period, period_jet_index = find_stone_period(jets, bottom_chamber, bottom_jet_index, bottom_shape_index)
    period_height = len(chamber_after_period) - bottom_height
    print(f"Period: {num_period_stones} stones, {period_height} height, {period_jet_index} jet index")
    # apply period N times up to the desired 'n'
    n_after_bottom = n - num_bottom_stones
    num_whole_periods = n_after_bottom // num_period_stones
    # count remaining stones in the last, incomplete period, and drop them
    remain_drop = n_after_bottom - num_whole_periods * num_period_stones
    print(f"n = {num_bottom_stones} + {num_whole_periods} * {num_period_stones} + {remain_drop}")
    chamber_height_before = len(chamber_after_period)
    top_chamber, _ = drop_stones(jets, period_jet_index, (n - remain_drop) % len(shapes), remain_drop, chamber_after_period)
    top_height = len(top_chamber) - chamber_height_before
    print(f"Top part: {remain_drop} stones, {top_height} height")
    # add all heights together
    return bottom_height + period_height * num_whole_periods + top_height


e.run_tests(2, part2)
e.run_main(2, part2)
