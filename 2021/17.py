#!/usr/bin/python3.8

from pyaoc import Env
import math
import re

e = Env(17)
e.T("target area: x=20..30, y=-10..-5", 45, 112)


def get_target(ln):
    r = re.compile('-?\d+')
    v = r.findall(ln)
    assert len(v) == 4
    return [int(x) for x in v]


def get_velocity_limits(xmin, xmax, ymin, ymax):
    """
    Velocity limits:
        Horizontal
        x = A * Vx - A + 1,     where A is the number of steps

        The lowest Vx for which we can hit the target, is the one where xmin = Vx^2 - Vx + 1.
        (after Vx steps, horizontal velocity will reach 0, so we put A = Vx, and make it reach xmin).

        From that equation,
        Vx(min) = (1 +- sqrt(-3 + 4 * xmin)) / 2   (rounded up to integer)
        Trivially
        Vx(max) = xmax

        Vertical
        Trivially
        Vy(min) = ymin

        If we shoot up (opposite of target), because the velocity is decreasing discretely by 1 each step,
        we will reach some step where velocity = 0 (the turning point). From the turning point, the velocity
        will keep decreasing by 1, which means that it will be the exact opposite of the velocity when
        climbing up at each step. That means that we will pass altitude 0 again, and the velocity at that
        point will be -Vy (the initial velocity). From altitude 0, the probe will keep falling with
        velocity -Vy-1, -Vy-2, ...

        Therefore, the max Vy that we can have and not overshoot the target on the descend of the parabola is
        Vy(max) = abs(ymin)
    """

    vxmin = int((1 + math.sqrt(-3 + 4 * xmin)) / 2 + 0.999)
    vxmax = xmax
    vymin = ymin
    vymax = abs(ymin)

    return vxmin, vxmax, vymin, vymax


def try_parabola(vx, vy, xmin, xmax, ymin, ymax):
    x = 0
    y = 0
    highest = 0
    hit = False
    while x < xmax and y > ymin:
        x += vx
        y += vy
        highest = max(highest, y)
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            hit = True
        vy -= 1
        vx = max(vx - 1, 0)
    return highest, hit


COUNT = 1
HIGHEST = 2


def run(input, what):
    xmin, xmax, ymin, ymax = get_target(input.get_valid_lines()[0])
    assert xmin > 0 and xmax > xmin and ymax < 0 and ymax > ymin
    vxmin, vxmax, vymin, vymax = get_velocity_limits(xmin, xmax, ymin, ymax)

    count = 0
    highest = None
    highest_vel = None

    for vx in range(vxmin, vxmax + 1):
        for vy in range(vymin, vymax + 1):
            height, hit = try_parabola(vx, vy, xmin, xmax, ymin, ymax)
            if hit:
                count += 1
                if highest is None or height > highest:
                    highest = height
                    highest_vel = (vx, vy)

    if what == HIGHEST:
        print(highest_vel)
        return highest
    return count


def part1(input):
    return run(input, HIGHEST)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return run(input, COUNT)


e.run_tests(2, part2)
e.run_main(2, part2)
