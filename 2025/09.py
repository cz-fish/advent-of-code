#!/usr/bin/python3.12

from pyaoc import Env

e = Env(9)
e.T("""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 50, 24)


def parse_input(input):
    points = []
    for ln in input.get_valid_lines():
        p = [int(x) for x in ln.split(',')]
        assert len(p) == 2
        points.append((p[0], p[1]))
    return points


def part1(input):
    points = parse_input(input)
    biggest = 0
    for first_i in range(len(points)):
        first = points[first_i]
        for second_i in range(first_i + 1, len(points)):
            second = points[second_i]
            size = (abs(second[0] - first[0]) + 1) * (abs(second[1] - first[1]) + 1)
            biggest = max(biggest, size)
    return biggest


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
