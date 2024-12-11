#!/usr/bin/python3.12

from pyaoc import Env

e = Env(11)
e.T("125 17", 55312, None)


def expand_stone(stone):
    new_stones = []
    if stone == 0:
        new_stones.append(1)
    else:
        s = str(stone)
        if len(s) % 2 == 0:
            left = int(s[:len(s)//2])
            right = int(s[len(s)//2:])
            new_stones.append(left)
            new_stones.append(right)
        else:
            new_stones.append(stone * 2024)
    return new_stones


#def blink(stones):
#    new_stones = []
#    for stone in stones:
#        new_stones.extend(expand_stone(stone))
#    return new_stones


def expand_and_cache(stone, max_gen, cache):
    if max_gen == 0:
        return 1
    if (stone, max_gen) in cache:
        return cache[(stone, max_gen)]
    expansion = expand_stone(stone)
    if (max_gen == 1):
        cache[(stone, max_gen)] = len(expansion)
        return len(expansion)
    total = 0
    for new_stone in expansion:
        total += expand_and_cache(new_stone, max_gen - 1, cache)
    cache[(stone, max_gen)] = total
    return total


def blink_with_cache(stones, max_gen):
    total = 0
    cache = {}
    for stone in stones:
        total += expand_and_cache(stone, max_gen, cache)
    return total


def part1(input):
    stones = input.get_all_ints()
    return blink_with_cache(stones, 25)
    #for gen in range(25):
    #    stones = blink(stones)
    #return len(stones)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    # blink 75 times
    stones = input.get_all_ints()
    return blink_with_cache(stones, 75)


e.run_tests(2, part2)
e.run_main(2, part2)
