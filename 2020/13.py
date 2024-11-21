#!/usr/bin/python3.8

from pyaoc import Env, Modular

e = Env(13)
e.T("""939
7,13,x,x,59,x,31,19""", 295, 1068781)
e.T("""0
17,x,13,19""", None, 3417)
e.T("""0
67,7,59,61""", None, 754018)
e.T("""0
67,x,7,59,61""", None, 779210)
e.T("""0
67,7,x,59,61""", None, 1261476)
e.T("""0
1789,37,47,1889""",  None, 1202161486)
e.T("""0
3,5""", None, 9)


def parse_input(inp):
    ln = inp.get_valid_lines()
    timestamp = int(ln[0])
    buses = [(int(bn), i) for i, bn in enumerate(ln[1].split(',')) if bn != 'x']
    return timestamp, buses


def part1(input):
    timestamp, buses = parse_input(input)
    busNums = [bus[0] for bus in buses]

    print(f"timestamp {timestamp}, buses: {busNums}")

    best = None
    for bus in busNums:
        nextDepart = bus - (timestamp % bus)
        if best is None or best[0] > nextDepart:
            best = [nextDepart, bus]

    result = best[0] * best[1]
    print(f"Part 1: next bus {best[1]} in {best[0]} minutes: {result}")
    return result


e.run_tests(1, part1)
e.run_main(1, part1)


# --- Part 2---
def part2(input):
    _, buses = parse_input(input)
    coef = [(-offset, bus) for bus, offset in buses]
    return Modular.chinese_remainders(coef)


e.run_tests(2, part2)
e.run_main(2, part2)
