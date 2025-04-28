#!/usr/bin/python3.12

from pyaoc import Env
from collections import Counter

e = Env(11)
e.T("ne,ne,ne", 3, None)
e.T("ne,ne,sw,sw", 0, None)
e.T("ne,ne,s,s", 2, None)
e.T("se,sw,se,sw,sw", 3, None)

e.T("ne,se", 2, None)
e.T("nw,ne,se", 1, None)
e.T("ne,ne,se,n", 3, None)
e.T("nw,nw,n", 3, None)


def distance(hops):
    d = {
        'n': (-2, 0),
        'nw': (-1, -1),
        'ne': (-1, 1),
        's': (2, 0),
        'sw': (1, -1),
        'se': (1, 1),
    }
    row = abs(sum([d[h][0] for h in hops]))
    col = abs(sum([d[h][1] for h in hops]))
    steps = col
    extra = (row - steps + 1) // 2
    if extra > 0:
        steps += extra
    print(row, col, steps, extra)
    return steps


def distance0(hops):
    # It's not this simple; 'se' and 'sw' together are just 1 's' step
    # d = {
    #     'n': (-1, 0),
    #     'nw': (-1, -1),
    #     'ne': (-1, 1),
    #     's': (1, 0),
    #     'sw': (1, -1),
    #     'se': (1, 1),
    # }
    # row = abs(sum([d[h][0] for h in hops]))
    # col = abs(sum([d[h][1] for h in hops]))
    # return max(row, col)
    dirs = Counter(hops)

    def cancel(a, b):
        elim = min(dirs[a], dirs[b])
        dirs[a] -= elim
        dirs[b] -= elim
        return elim
    
    cancel("nw", "se")
    cancel("ne", "sw")
    cancel("n", "s")
    dirs["n"] += cancel("nw", "ne") # NW + NE = N
    dirs["s"] += cancel("sw", "se") # SW + SE = S
    return sum(dirs.values())

    elim = min(dirs["se"], dirs["sw"])
    dirs["se"] -= elim
    dirs["sw"] -= elim
    dirs["s"] += elim
    elim = min(dirs["ne"], dirs["nw"])
    dirs["ne"] -= elim
    dirs["nw"] -= elim
    dirs["n"] += elim
    vert = abs(dirs["n"] + dirs["ne"] + dirs["nw"] - dirs["s"] - dirs["se"] - dirs["sw"])
    hor = abs(dirs["nw"] + dirs["sw"] - dirs["ne"] - dirs["se"])
    # vertical steps are easy, we can go directly N or S
    # horizontal steps are trickier, we always need even number of steps
    if hor % 2 == 1:
        hor += 1
    return max(vert, hor)


def part1(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    hops = lines[0].split(',')
    return distance(hops)

# 515 too low
# 580 too low

e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
