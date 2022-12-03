#!/usr/bin/python3.8

from aoc import Env

e = Env(3)
e.T("""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""", 157, 70)

def priority(item):
    if item >= 'a' and item <= 'z':
        return ord(item) - ord('a') + 1
    elif item >= 'A' and item <= 'Z':
        return ord(item) - ord('A') + 27
    else:
        assert False, f'invalid item {item}'


def misplaced_item_priority(rucksack):
    n = len(rucksack)
    assert n % 2 == 0, f'rucksack "{rucksack}" not even length'
    left = set(c for c in rucksack[:n//2])
    right = set(c for c in rucksack[n//2:])
    same = list(left.intersection(right))
    assert len(same) == 1, f'number of same items is not 1 but {len(same)} ({same}) "{rucksack}"'
    return priority(same[0])


def part1(input):
    lines = input.get_valid_lines()
    return sum([misplaced_item_priority(line) for line in lines])


e.run_tests(1, part1)
e.run_main(1, part1)


def badge_priority(rucksacks):
    assert len(rucksacks) == 3
    all = None
    for i in range(3):
        s = set(c for c in rucksacks[i])
        if all is None:
            all = s
        else:
            all = all.intersection(s)
    assert len(all) == 1, f'Expected to find single badge, found {all} among rucksacks {rucksacks}'
    return priority(list(all)[0])


def part2(input):
    rucksacks = input.get_valid_lines()
    n = len(rucksacks)
    assert n % 3 == 0, f'Number of rucksacks ({n}) is not multiple of 3'
    return sum([badge_priority(rucksacks[i:i+3]) for i in range(0, n, 3)])


e.run_tests(2, part2)
e.run_main(2, part2)