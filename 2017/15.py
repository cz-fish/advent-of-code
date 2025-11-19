#!/usr/bin/python3.12

from pyaoc import Env

e = Env(15)
e.T("""Generator A starts with 65
Generator B starts with 8921""", 588, 309)

factors = [16807, 48271]
modulus = 2147483647
# primitive root 7
judge_bits = 0xffff


def multiply_modulo_mersenne_prime(a, b, n, mod):
    m = a * b
    s = (m >> n) + (m & mod)
    if s == mod:
        s -= 1
    return s

def multiply_modulo(a, b, mod):
    return (a * b) % mod


def part1(input):
    seeds = input.get_ints_tolerant()
    N = 40000000
    #N = 1000
    n = 31
    a = seeds[0]
    b = seeds[1]
    count = 0
    for i in range(N):
        #x = multiply_modulo_mersenne_prime(a, factors[0], n, modulus)
        #y = multiply_modulo_mersenne_prime(b, factors[1], n, modulus)
        a = multiply_modulo(a, factors[0], modulus)
        b = multiply_modulo(b, factors[1], modulus)
        #assert x == a
        #assert y == b
        if (a & judge_bits) == (b & judge_bits):
            count += 1
    return count


e.run_tests(1, part1)
e.run_main(1, part1)


def multiply_modulo_even(a, b, mod, mask):
    while True:
        a = (a * b) % mod
        if (a & mask == 0):
            return a


def part2(input):
    seeds = input.get_ints_tolerant()
    N = 5000000
    # a: v % 4 == 0, b: v % 8 == 0
    n = 31
    a = seeds[0]
    b = seeds[1]
    count = 0
    for i in range(N):
        a = multiply_modulo_even(a, factors[0], modulus, 3)
        b = multiply_modulo_even(b, factors[1], modulus, 7)
        if (a & judge_bits) == (b & judge_bits):
            count += 1
    return count


e.run_tests(2, part2)
e.run_main(2, part2)
