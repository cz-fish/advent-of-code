#!/usr/bin/python3.8

from pyaoc import Env

e = Env(25)
e.T("""1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""", "2=-1=0", None)


snafu = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}

inverse = {
    2: '2',
    1: '1',
    0: '0',
    3: '=',
    4: '-',
}

def decode_snafu(nr):
    chars = [c for c in nr][::-1]
    coef = 1
    val = 0
    for c in chars:
        digit = snafu[c]
        val += coef * digit
        coef *= 5
    return val


def encode_snafu(val):
    if val == 0:
        return "0"
    digits = []
    while val > 0:
        d = val % 5
        if d > 2:
            val += 5
        val //= 5
        digits.append(inverse[d])
    return ''.join(digits[::-1])


def part1(input):
    total = 0
    for ln in input.get_valid_lines():
        total += decode_snafu(ln)
    return encode_snafu(total)


e.run_tests(1, part1)
e.run_main(1, part1)

