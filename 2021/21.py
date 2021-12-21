#!/usr/bin/python3.8

from aoc import Env
from collections import deque

e = Env(21)
e.T("""Player 1 starting position: 4
Player 2 starting position: 8""", 739785, 444356092776315)


def play_deterministic_dice(p1, p2):
    rolls = 0
    dice_v = 1
    pos = [p1, p2]
    points = [0, 0]
    player = 0

    while points[0] < 1000 and points[1] < 1000:
        r = dice_v
        dice_v = dice_v % 100 + 1
        r += dice_v
        dice_v = dice_v % 100 + 1
        r += dice_v
        dice_v = dice_v % 100 + 1
        rolls += 3
        p = (pos[player] + r - 1) % 10 + 1
        pos[player] = p
        points[player] += p
        player = (player + 1) % 2

    return points[0], points[1], rolls


def part1(input):
    x = input.get_all_ints()
    p1 = x[1]
    p2 = x[3]
    a, b, c = play_deterministic_dice(p1, p2)
    res = c * min(a, b)
    return res


e.run_tests(1, part1)
e.run_main(1, part1)


"""
possible rolls
1,1,1 = 3
...
3,3,3 = 9
-> 7 different outcomes with different weights (number of universes)

average points per move ~5
average number of moves to win ~4-5, x2 ~ 8-9
7 ** 8-9 ~ 5M-40M moves to simulate ?
"""

weights = {i: 0 for i in range(3, 10)}
for i in range(1,4):
    for j in range(1, 4):
        for k in range(1, 4):
            weights[i+j+k] += 1


def play_dirac_dice(p1, p2):
    #counter = 0
    # player, p1 pos, p2 pos, p1 score, p2 score, universes
    st = (0, [p1, p2], [0, 0], 1)
    d = deque()
    d.append(st)
    wins = [0, 0]
    while d:
        player, pos, points, universes = d.popleft()
        #counter += 1
        #if counter % 100000 == 0:
        #    print(counter, points)
        for roll, cases in weights.items():
            newpos = pos[player]
            newpos = (newpos - 1 + roll) % 10 + 1
            newpoints = points[player]
            newpoints += newpos
            if newpoints >= 21:
                wins[player] += universes * cases
            else:
                a = pos[:]
                a[player] = newpos
                b = points[:]
                b[player] = newpoints
                d.append((
                    (player + 1) % 2,
                    a,
                    b,
                    universes * cases
                ))
    return wins[0], wins[1]


def part2(input):
    x = input.get_all_ints()
    p1 = x[1]
    p2 = x[3]
    a, b = play_dirac_dice(p1, p2)
    res = max(a, b)
    return res


e.run_tests(2, part2)
e.run_main(2, part2)
