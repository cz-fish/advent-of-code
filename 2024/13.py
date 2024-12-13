#!/usr/bin/python3.12

from pyaoc import Env
import re

e = Env(13)
e.T("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""", 480, 875318608908)
# in part 1, 1st and 3rd are winnable. In part 2, 2nd and 4th are winnable

e.T("""Button A: X+74, Y+20
Button B: X+14, Y+88
Prize: X=1580, Y=5480""", 90, 0)


button_re = re.compile(r'Button .: X\+(\d+), Y\+(\d+)')
prize_re = re.compile(r'Prize: X=(\d+), Y=(\d+)')

def make_machine(lines):
    assert len(lines) == 3
    b_a = button_re.match(lines[0])
    assert b_a is not None
    b_b = button_re.match(lines[1])
    assert b_b is not None
    pr = prize_re.match(lines[2])
    assert pr is not None
    button_a = (int(b_a.group(1)), int(b_a.group(2)))
    button_b = (int(b_b.group(1)), int(b_b.group(2)))
    prize = (int(pr.group(1)), int(pr.group(2)))
    return button_a, button_b, prize


def cost_to_win(b_a, b_b, prize) -> int:
    A = min(100, max(prize[0] // b_a[0], prize[1] // b_a[1]))
    best_cost = 0
    for a in range(A):
        cost = a * 3
        if best_cost > 0 and cost > best_cost:
            # cannot find a cheaper solution than we already have
            break
        rem_x = prize[0] - a * b_a[0]
        rem_y = prize[1] - a * b_a[1]
        if rem_x < 0 or rem_y < 0:
            # already overshot with just button a
            break
        b = rem_x // b_b[0]
        if b_b[0] * b != rem_x or b_b[1] * b != rem_y:
            # values don't add up
            continue
        # we have a solution
        cost += b
        if best_cost == 0 or cost < best_cost:
            best_cost = cost
    return best_cost


def part1(input):
    machines = [make_machine(m) for m in input.get_groups()]
    return sum([cost_to_win(b_a, b_b, prize) for b_a, b_b, prize in machines])


e.run_tests(1, part1)
e.run_main(1, part1)


def large_cost_to_win(b_a, b_b, prize) -> int:
    # check if vectors a and b are parallel
    if b_a[0] * b_b[1] == b_a[1] * b_b[0]:
        print(f"Vectors {b_a} and {b_b} are parallel; need to add a solution for that case")
        assert False
    if b_b[0] == 0:
        print(f"Bx is zero for {b_a} and {b_b}; need to add solution for that case")
        assert False

    N = (prize[1] - b_b[1] * prize[0] / b_b[0]) / (b_a[1] - b_a[0] * b_b[1] / b_b[0])
    M = (prize[0] - N * b_a[0]) / b_b[0]
    # Add 0.1 to fight rounding errors. Is there any better formula that only uses integer math?
    n = int(N + 0.1)
    m = int(M + 0.1)
    if b_a[0] * n + b_b[0] * m == prize[0] and b_a[1] * n + b_b[1] * m == prize[1]:
        #print(f"Found solution for {b_a}, {b_b}, {prize} with n {n}, m {m}")
        return 3 * n + m
    else:
        #print(f"No solution for {b_a}, {b_b}, {prize} with n {n} ({N}), m {m} ({M})")
        return 0


def part2(input):
    machines = [make_machine(m) for m in input.get_groups()]
    # Try without addition first; results should match part1
    all_good = True
    part1_answer = 0
    for machine in machines:
        a, b, p = machine
        x = cost_to_win(a, b, p)
        y = large_cost_to_win(a, b, p)
        if x != y:
            print(f"Mismatch for machine: {a} {b} {p}. Got {y}, expecting {x}")
            all_good = False
        else:
            part1_answer += y
    print(f"Without addition: {part1_answer}")
    assert all_good

    add = 10000000000000
    return sum([large_cost_to_win(b_a, b_b, (prize[0] + add, prize[1] + add)) for b_a, b_b, prize in machines])


e.run_tests(2, part2)
e.run_main(2, part2)

# 67678723782557 too low
