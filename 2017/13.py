#!/usr/bin/python3.12

from pyaoc import Env

e = Env(13)
e.T("""0: 3
1: 2
4: 4
6: 4""", 24, 10)


def parse_input(input):
    fire = {}
    for ln in input.get_valid_lines():
        left, right = ln.split(": ")
        k = int(left)
        assert k not in fire
        fire[k] = int(right)
    return fire


def part1(input):
    firewalls = parse_input(input)
    total = 0
    for layer, size in firewalls.items():
        # [0123]
        #      [210]
        # size 4, back in 6
        # [012]
        #     [10]
        # size 3, back in 4
        period = 2 * (size - 1)
        if layer % period == 0:
            total += layer * size
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def caught(delay, layers):
    # for each layer
    #  (layer + delay) % period > 0
    return any([
        (layer + delay) % (2 * size - 2) == 0
        for layer, size in layers.items()
    ])


def part2(input):
    firewalls = parse_input(input)
    delay = 0
    while True:
        if not caught(delay, firewalls):
            return delay
        delay += 1


e.run_tests(2, part2)
e.run_main(2, part2)
