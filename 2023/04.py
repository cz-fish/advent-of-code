#!/usr/bin/python3.8

from aoc import Env

e = Env(4)
e.T("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""", 13, 30)

def parse_cards(input):
    cards = []
    for ln in input.get_valid_lines():
        _, card = ln.split(": ")
        win, have = card.split(" | ")
        cards.append(([int(x) for x in win.split(' ') if x], [int(x) for x in have.split(' ') if x]))
    return cards


def part1(input):
    cards = parse_cards(input)
    points = 0
    for win, have in cards:
        nums = set(win)
        nums = nums.intersection(set(have))
        if nums:
            points += 2 ** (len(nums) - 1)
    return points


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    cards = parse_cards(input)
    counts = [1] * len(cards)
    for card_no, (win, have) in enumerate(cards):
        nums = set(win)
        nums = nums.intersection(set(have))
        points = len(nums)
        for i in range(1, points + 1):
            if card_no + i >= len(counts):
                break
            counts[card_no + i] += counts[card_no]
    return sum(counts)


e.run_tests(2, part2)
e.run_main(2, part2)
