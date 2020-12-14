#!/usr/bin/python3.8

from aoc import Env

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
def chinese_remainders(buses):

    def bezout(num, base):
        # Extended Euclidean algorithm
        s = 0
        s_prev = 1
        t = 1
        t_prev = 0
        r = base
        r_prev = num
        while r != 0:
            q = r_prev // r
            r_prev, r = r, r_prev - q * r
            s_prev, s = s, s_prev - q * s
            t_prev, t = t, t_prev - q * t
        return s_prev, t_prev

    a1 = 0
    # First equation
    # x = 0 (mod <first bus>)
    # N1 is the product of all bus numbers folded so far
    N1 = buses[0][0]
    # For all remaining buses, one by one
    for n2, a2neg in buses[1:]:
        # Next equation
        # x = -offset (mod <i-th bus>)
        # `n2` is the i-th bus number
        # `a2neg` is the time offset. Because this bus arrives
        # at time `x + offset`, the right side is `-offset`.
        a2 = -a2neg
        # Determine Bezout coefficients for the i-th equation and
        # the product of all equations before i.
        m1, m2 = bezout(N1, n2)
        # Chinese remainder theorem:
        # x = a1 * m2 * n2 + a2 * M1 * N1
        x = a1 * m2 * n2 + a2 * m1 * N1
        # There are infinitely many `x`. We want the one between
        # 0 and N1 - hence modulo
        N1 *= n2
        x = x % N1
        # In the next iteration, x becomes the coefficient of the folded term
        a1 = x
    # The last x is the result
    return a1


def part2(input):
    _, buses = parse_input(input)
    return chinese_remainders(buses)


e.run_tests(2, part2)
e.run_main(2, part2)
