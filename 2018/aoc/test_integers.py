from aoc import Integers

def test_prime_factors():
    assert Integers.prime_factors(0) == []
    assert Integers.prime_factors(1) == []
    assert Integers.prime_factors(2) == [2]
    assert Integers.prime_factors(4) == [2, 2]
    assert Integers.prime_factors(13) == [13]
    assert Integers.prime_factors(887) == [887]
    assert Integers.prime_factors(10551287) == [127, 251, 331]


def test_all_divisors():
    assert Integers.all_divisors(0) == [1]
    assert Integers.all_divisors(1) == [1]
    assert Integers.all_divisors(2) == [1, 2]
    assert Integers.all_divisors(4) == [1, 2, 4]
    assert Integers.all_divisors(12) == [1, 2, 3, 4, 6, 12]
    assert Integers.all_divisors(887) == [1, 887]
    assert Integers.all_divisors(10551287) == [1, 127, 251, 331, 31877, 42037, 83081, 10551287]
