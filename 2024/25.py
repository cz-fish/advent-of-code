#!/usr/bin/python3.12

from pyaoc import Env

e = Env(25)
e.T("""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""", 3, None)


def get_pattern(g):
    pattern = []
    for col in range(len(g[0])):
        line = ''.join([g[i][col] for i in range(len(g))])
        pattern.append(len(line.replace('.', '')) - 1)
    return pattern


def parse_input(input):
    locks = []
    keys = []
    for g in input.get_groups():
        if g[0] == '#####':
            locks.append(get_pattern(g))
        else:
            keys.append(get_pattern(g))
    return locks, keys


def match(lock, key):
    assert len(lock) == len(key)
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True


def part1(input):
    locks, keys = parse_input(input)
    combos = 0
    for lock in locks:
        for key in keys:
            if match(lock, key):
                combos += 1
    return combos


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
