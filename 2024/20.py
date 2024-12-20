#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import defaultdict

e = Env(20, param=(100, 100))
e.T("""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""", 14+14+2+4+2+3+1+1+1+1+1,
    32+31+29+39+25+23+20+19+12+14+22+4+3,
    param=(0, 50))


def find_start_end(g):
    start = None
    end = None
    for row in range(g.h):
        for col in range(g.w):
            if g.get(row, col) == 'S':
                assert start is None
                start = (row, col)
                if end: break
            elif g.get(row, col) == 'E':
                assert end is None
                end = (row, col)
                if start: break
    assert start is not None
    assert end is not None
    return start, end


def find_cheats(g, start, end):
    pos = start
    cost = 0
    path = [pos]
    costs = {pos: 0}
    cheats = []
    while pos != end:
        nextpos = None
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nr, nc = (pos[0]+dr, pos[1]+dc)
            if g.get(nr, nc) == '#':
                # possible cheat
                if g.is_in(nr + dr, nc + dc) and g.get(nr + dr, nc + dc) != '#':
                    cheats.append((pos, (nr+dr, nc+dc)))
            else:
                if (nr, nc) not in costs:
                    assert nextpos is None, f"More than one exit from {pos}"
                    nextpos = (nr, nc)
        assert nextpos is not None, f"No exit from {pos}"
        pos = nextpos
        assert pos not in costs
        cost += 1
        costs[pos] = cost
        path.append(pos)
    return path, costs, cheats


def count_savings(path, costs, cheats, save_limit):
    total_cost = costs[path[-1]]
    count = 0
    count_by_saving = defaultdict(int)
    for src, tgt in cheats:
        src_dist = total_cost - costs[src]
        tgt_dist = total_cost - costs[tgt]
        # -2 because it costs 2 steps to go through the cheat
        save = src_dist - tgt_dist - 2
        if save >= save_limit:
            count += 1
        if save > 0:
            count_by_saving[save] += 1
    stats = list(count_by_saving.items())
    stats.sort(key=lambda x:(x[0], -x[1]))
    #for k, v in stats:
    #    print(f"{v} cheats saving {k} steps")
    return count


def part1(input):
    g = Grid(input.get_valid_lines())
    start, end = find_start_end(g)
    save_limit = e.get_param()[0]
    path, costs, cheats = find_cheats(g, start, end)
    return count_savings(path, costs, cheats, save_limit)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
