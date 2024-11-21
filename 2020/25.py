#!/usr/bin/python3.8

from pyaoc import Env

e = Env(25)
e.T("""5764801
17807724""", 14897079, None)

def get_loop_number(key):
    v = 1
    for i in range(20201227):
        v = (v * 7) % 20201227
        if v == key:
            return i + 1
    assert False


def loop(start, loops):
    v = 1
    for _ in range(loops):
        v = (v * start) % 20201227
    return v


def part1(input):
    ln = input.get_valid_lines()
    A = int(ln[0])
    B = int(ln[1])
    # A = 7 ** n mod 20201227
    # B = 7 ** m mod 20201227
    # 20201227 is prime
    n = get_loop_number(A)
    m = get_loop_number(B)
    print(f"Loop numbers: {n}, {m}")
    return loop(A, m)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
