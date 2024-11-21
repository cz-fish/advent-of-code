#!/usr/bin/python3.8

from pyaoc import Env

e = Env(23)
e.T("""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""", 110, 20)


def load_state(input):
    minmax = [0, 0, 0, 0]
    elves = set()
    for y, ln in enumerate(input.get_valid_lines()):
        for x, c in enumerate(ln):
            if c == '#':
                elves.add((x, y))
                if x > minmax[2]:
                    minmax[2] = x
                if y > minmax[3]:
                    minmax[3] = y
    return elves, minmax


around = [
    (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)
]

directions = [
    [0, 1, 2], # N
    [4, 5, 6], # S
    [6, 7, 0], # W
    [2, 3, 4], # E
]

step_dir = [
    (0, -1), # N
    (0, 1), # S
    (-1, 0), # W
    (1, 0), # E
]


def move(elves, step):
    propo = {}
    stopped = set()

    for elf in elves:
        # look all around the elf
        sur = [1 if (elf[0] + p[0], elf[1] + p[1]) in elves else 0 for p in around]
        if sum(sur) == 0:
            stopped.add(elf)
            continue
        for d in range(4):
            # the orde of instructions rotates every step
            dir_index = (d + step) % 4
            direction = directions[dir_index]
            if sur[direction[0]] + sur[direction[1]] + sur[direction[2]] == 0:
                # elf can move in the direction dir_index
                new_pos = (elf[0] + step_dir[dir_index][0], elf[1] + step_dir[dir_index][1])
                if new_pos not in propo:
                    propo[new_pos] = set()
                propo[new_pos].add(elf)
                break
        else:
            # elf is blocked in all 4 directions
            stopped.add(elf)

    new_elves = set()
    someone_moved = False

    for pos, candidates in propo.items():
        if len(candidates) == 1:
            new_elves.add(pos)
            someone_moved = True
        else:
            for elf in candidates:
                new_elves.add(elf)
    for elf in stopped:
        new_elves.add(elf)

    return new_elves, someone_moved


def spread_size(elves):
    minmax = None
    for elf in elves:
        if minmax is None:
            minmax = [elf[0], elf[1], elf[0], elf[1]]
        else:
            if elf[0] < minmax[0]:
                minmax[0] = elf[0]
            if elf[1] < minmax[1]:
                minmax[1] = elf[1]
            if elf[0] > minmax[2]:
                minmax[2] = elf[0]
            if elf[1] > minmax[3]:
                minmax[3] = elf[1]
    return minmax


def part1(input):
    elves, minmax = load_state(input)
    print(f"Start: {len(elves)} elves, minmax {minmax}")
    for i in range(10):
        elves, _ = move(elves, i)
    minmax = spread_size(elves)
    size = (minmax[2] - minmax[0] + 1) * (minmax[3] - minmax[1] + 1)
    print(f"{len(elves)} elves in space of size {size}")
    return size - len(elves)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    elves, _ = load_state(input)
    round = 0
    while True:
        elves, moved = move(elves, round)
        round += 1
        if not moved:
            break
    return round


e.run_tests(2, part2)
e.run_main(2, part2)
