from aoc import Modular

def test_bezout_identity():
    assert(Modular.bezout(3, 5) == (2, -1))


def test_multiplicative_inverse():
    assert(Modular.mult_inverse(17, 19) == 9)


def test_chinese_remainders():
    """
        x = 0 (mod 17)
        x = -2 (mod 13)
        x = -3 (mod 19)
        -> x = 3417
    """
    coef = [(0, 17), (-2, 13), (-3, 19)]
    assert(Modular.chinese_remainders(coef) == 3417)
