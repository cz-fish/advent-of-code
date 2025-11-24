#!/usr/bin/python3.12

from pyaoc import Env

e = Env(17)
e.T("3", 638, None)
e.T("3", None, 1, param = 1)
e.T("3", None, 2, param = 2)
e.T("3", None, 2, param = 3)
e.T("3", None, 5, param = 5)
e.T("3", None, 5, param = 8)
e.T("3", None, 9, param = 9)


def part1(input):
    v = input.get_ints()
    assert len(v) == 1
    stride = v[0]
    buf = [0]
    pos = 0
    for step in range(2017):
        pos = (pos + stride) % len(buf) + 1
        val = step + 1
        buf = buf[:pos] + [val] + buf[pos:]
    return buf[(pos + 1) % len(buf)]


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    # value after 0 after 50M cycles
    v = input.get_ints()
    assert len(v) == 1
    stride = v[0]
    max_iter = e.get_param()
    if max_iter is None:
        max_iter = 50000000
    # insert_pos = (pos + stride) % len(buf)
    # looking for the last iteration before 50M, in which insert_pos = 0
    # 0 = (pos + stride) % (N + 1)
    pos = 0
    result = None
    for c in range(max_iter):
        val = c + 1
        pos = (pos + stride) % val
        if pos == 0:
            result = val
        pos += 1
    return result


e.run_tests(2, part2)
e.run_main(2, part2)
