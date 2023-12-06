#!/usr/bin/python3.8

from aoc import Env
import re
import math

e = Env(6)
e.T("""Time:      7  15   30
Distance:  9  40  200""", 288, 71503)

def hold_button(time, dist_to_beat):
    """
    time T, dist_to_beat D
    hold the button for K milliseconds
    distance x = K * (T-K) = -K*K* + T*K
        x > D
    => -K^2 + T*K > D
    => -K^2 + T*K - D > 0
    k1,k2 = (-T +- sqrt(T*T - 4*D)) / (-2) = (T +- sqrt(T^2 - 4*D)) / 2
    """
    disc = time * time - 4 * dist_to_beat
    assert disc > 0, f"Discriminant of quadratic equation not positive: {disc}"
    k1 = (time - math.sqrt(disc)) / 2
    k2 = (time + math.sqrt(disc)) / 2
    # round k1 up and k2 down to nearest integer
    K1 = math.ceil(k1)
    K2 = math.floor(k2)
    # make sure to satisfy strict inequality to win and not just tie
    if K1 == k1:
        K1 += 1
    if K2 == k2:
        K2 -= 1
    if K2 < K1:
        K2 = K1
    return K1, K2


def part1(input):
    times_ln, dists_ln = input.get_valid_lines()
    times = [int(x) for x in re.findall(r'\d+', times_ln)]
    dists = [int(x) for x in re.findall(r'\d+', dists_ln)]
    assert len(times) == len(dists)

    product = 1
    for i in range(len(times)):
        time = times[i]
        dist_to_beat = dists[i]
        k1, k2 = hold_button(time, dist_to_beat)
        #print(f"time {time} dist_to_beat {dist_to_beat}, hold from {k1} to {k2} ({k2-k1+1})")
        product *= k2 - k1 + 1
    return product


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    times_ln, dists_ln = input.get_valid_lines()
    times_ln = times_ln.replace(' ', '')
    dists_ln = dists_ln.replace(' ', '')
    times = [int(x) for x in re.findall(r'\d+', times_ln)]
    dists = [int(x) for x in re.findall(r'\d+', dists_ln)]
    assert len(times) == len(dists)
    assert len(times) == 1
    
    time = times[0]
    dist_to_beat = dists[0]
    k1, k2 = hold_button(time, dist_to_beat)
    #print(f"time {time} dist_to_beat {dist_to_beat}, hold from {k1} to {k2} ({k2-k1+1})")
    return k2 - k1 + 1


e.run_tests(2, part2)
e.run_main(2, part2)
