#!/usr/bin/python3.12

from pyaoc import Env
from knot_hash import twist, make_dense, dense_as_hex

e = Env(10, param=256)
e.T("3, 4, 1, 5", 12, None, param=5)
e.T("", None, "a2582a3a0e66e6e86e3812dcb672a272", param=256)
e.T("AoC 2017", None, "33efeb34ea91902bb2f59c9920caa6cd", param=256)
e.T("1,2,3", None, "3efbe78a8d82f29979031a4aa0b16a9d", param=256)
e.T("1,2,4", None, "63960835bcdc130f0b66d7ff4f6a5a8e", param=256)


def part1(input):
    size = e.get_param()
    loop = list(range(size))
    lengths = input.get_all_ints()
    loop = twist(loop, lengths)
    return loop[0] * loop[1]


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    size = e.get_param()
    loop = list(range(size))
    # use input as ascii string
    lines = input.get_valid_lines()
    assert len(lines) <= 1
    if not lines:
        lengths = []
    else:
        payload = lines[0]
        lengths = [ord(c) for c in payload]
    # append lengths 17, 31, 73, 47, 23
    lengths.extend([17, 31, 73, 47, 23])
    # apply hash 64 times, preserving pos and skip
    twist(loop, lengths, 64)
    # reduce to dense hash by xoring blocks of 16 numbers - first 16 numbers xord together is first char of dense hash
    dense = make_dense(loop)
    # print dense hash as lower case hex string
    return dense_as_hex(dense)


e.run_tests(2, part2)
e.run_main(2, part2)
