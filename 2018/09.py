#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict

e = Env(9)
e.T("9 players; last marble is worth 25 points", 32, None, True)
e.T("10 players; last marble is worth 1618 points", 8317, None)
e.T("13 players; last marble is worth 7999 points", 146373, None)
e.T("17 players; last marble is worth 1104 points", 2764, None)
e.T("21 players; last marble is worth 6111 points", 54718, None)
e.T("30 players; last marble is worth 5807 points", 37305, None)


class Marble():
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None


def play_game(players, max_marble):
    points = defaultdict(int)
    zero = Marble(0)
    zero.next = zero
    zero.prev = zero
    circle = zero
    for i in range(1, max_marble + 1):
        if i % 23 == 0:
            # collect points
            player = i % players
            points[player] += i
            for x in range(7):
                circle = circle.prev
            points[player] += circle.val
            left = circle.prev
            right = circle.next
            left.next = right
            right.prev = left
            circle = right
        else:
            # place marble
            m = Marble(i)
            left = circle.next
            right = left.next
            m.prev = left
            m.next = right
            left.next = m
            right.prev = m
            circle = m

    if e.get_param():
        # print circle
        vals = [circle.val]
        start = circle.next
        while start != circle:
            vals += [start.val]
            start = start.next
        print(vals)
    
    max_score = max(points.values())
    return max_score


def part1(input):
    players, max_marble = input.get_all_ints()
    return play_game(players, max_marble)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    players, max_marble = input.get_all_ints()
    return play_game(players, max_marble * 100)


e.run_tests(2, part2)
e.run_main(2, part2)
