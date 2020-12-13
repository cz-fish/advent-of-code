#!/usr/bin/python3.8

from aoc import Input

inp = Input('input13.txt', [
    """939
7,13,x,x,59,x,31,19""",  # 1068781
    """0
17,x,13,19""",  # 3417
    """0
67,7,59,61""",  # 754018
    """0
67,x,7,59,61""",  # 779210
    """0
67,7,x,59,61""",  # 1261476
    """0
1789,37,47,1889""",  # 1202161486
    """0
3,5"""  # 9
])

# inp.use_test(0)


def parse_input(inp):
    ln = inp.get_valid_lines()
    timestamp = int(ln[0])
    buses = [(int(bn), i) for i, bn in enumerate(ln[1].split(',')) if bn != 'x']
    return timestamp, buses


timestamp, buses = parse_input(inp)
busNums = [bus[0] for bus in buses]

print(f"timestamp {timestamp}, buses: {busNums}")

### Part 1
best = None
for bus in busNums:
    nextDepart = bus - (timestamp % bus)
    if best is None or best[0] > nextDepart:
        best = [nextDepart, bus]

print(f"Part 1: next bus {best[1]} in {best[0]} minutes: {best[0] * best[1]}")


### Part 2
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


do_tests = False
# do_tests = True
if do_tests:
    for case in range(7):
        inp.use_test(case)
        _, buses = parse_input(inp)
        solution = chinese_remainders(buses)
        print(f"{buses}\n-> {solution}")
else:
    solution = chinese_remainders(buses)
    print(f"Part 2: {solution}")
