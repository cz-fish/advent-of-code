#!/usr/bin/python3.8

from aoc import Env
from collections import deque, defaultdict

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


def play_dirac_differently(p1, p2):
    scores = [
        [defaultdict(int) for _ in range(10)]
        for _ in range(21)
    ]
    for points in range(20, -1, -1):
        for pos in range(10):
            for roll, cases in weights.items():
                nextpos = (pos + roll) % 10
                getpoints = nextpos + 1
                newscore = points + getpoints
                if newscore >= 21:
                    scores[points][pos][1] += cases
                else:
                    for k, v in scores[newscore][nextpos].items():
                        scores[points][pos][k + 1] += v * cases
    for x in range(10):
        print('pos', x, sorted(list(scores[0][x].items())))
    print('--------')
    print(p1, p2)

    start_p1 = sorted(scores[0][p1 - 1].items(), key=lambda x:-x[0])
    start_p2 = sorted(scores[0][p2 - 1].items(), key=lambda x:-x[0])

    #start_p1 = sorted(scores[0][p1 - 1].items())
    #start_p2 = sorted(scores[0][p2 - 1].items())

    accu_p1 = {}
    a = 0
    for s, t in start_p1:
        a += t
        accu_p1[s] = a
    accu_p2 = {}
    a = 0
    for s, t in start_p2:
        a += t
        accu_p2[s] = a
    print(accu_p1.items())
    print(accu_p2.items())

    #print(p1, start_p1)
    #print(p2, start_p2)
    total_p1 = 0
    for steps, v in start_p1:
        x = accu_p2[steps] if steps in accu_p2 else 0
        total_p1 += v * x
        """
        # p1 won in 'steps' steps in 'v' universes
        # but only if p2 didn't win first. p2 must have rolled one of 3^3^steps combinations
        # except for those that would allow p2 to win in fewer than 'steps' steps
        s2 = (3 ** 3) ** (steps - 1)
        if steps - 1 in accu_p2:
            s2 -= accu_p2[steps - 1]
        total_p1 += v * s2
        print(f"p1 finished in {steps} steps {v} times. p2 could roll {s2} combinations and lose")
        """
        print(f"p1, steps {steps}, {v} * {x} = {v * x} ... {total_p1}")

    total_p2 = 0
    for steps, v in start_p2:
        x = accu_p1[steps + 1] if steps + 1 in accu_p1 else 0
        total_p2 += v * x
        """
        s1 = (3 ** 3) ** (steps)
        if steps in start_p1:
            s1 -= accu_p1[steps]
        total_p2 += v * s1
        print(f"p2 finished in {steps} steps {v} times. p1 could roll {s1} combinations and lose")
        """
        print(f"p2, steps {steps}, {v} * {x} = {v * x} ... {total_p2}")

    return max(total_p1, total_p2)


def part2(input):
    x = input.get_all_ints()
    p1 = x[1]
    p2 = x[3]
    return max(play_dirac_dice(p1, p2))
    return play_dirac_differently(p1, p2)


e.run_tests(2, part2)
e.run_main(2, part2)
