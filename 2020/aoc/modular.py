from typing import List, Tuple


class Modular:
    @classmethod
    def bezout(cls, m: int, n: int) -> Tuple[int, int]:
        """Bezout's identity
        For
            a * m + b * n = 1,
        find some integers a and b that satisfy the equation.
        There are infinitely many solutions."""

        # Extended Euclidean algorithm
        s = 0
        s_prev = 1
        t = 1
        t_prev = 0
        r = n
        r_prev = m
        while r != 0:
            q = r_prev // r
            r_prev, r = r, r_prev - q * r
            s_prev, s = s, s_prev - q * s
            t_prev, t = t, t_prev - q * t
        return s_prev, t_prev

    @classmethod
    def mult_inverse(cls, a: int, n: int) -> int:
        """For an integer `a` and base `n`, return multiplicative
        inverse of `a` modulo `n`, such that
            a * a' = 1 (mod n)"""
        res, _ = Modular.bezout(a, n)
        return res % n

    @classmethod
    def chinese_remainders(cls, coef: List[Tuple[int, int]]) -> int:
        """Chinese Remainder Theorem
        Given a list of modular equations
            x = a_1 (mod n_1)
            x = a_2 (mod n_2)
            ...
            x = a_k (mod n_k)
        Find x that satisfies all of them.
        The input parameter `coef` is a list of tuples (`a_j`, `n_j`)
        for each equation."""

        a1 = coef[0][0]
        # First equation
        # x = a_1 (mod n_1)
        # N1 is the product of all `n` numbers folded so far
        N1 = coef[0][1]
        # For all remaining equations, one by one
        for a2, n2 in coef[1:]:
            # Determine Bezout coefficients for the i-th equation and
            # the product of all equations before i.
            m1, m2 = Modular.bezout(N1, n2)
            # Chinese remainder theorem:
            # x = a1 * m2 * n2 + a2 * M1 * N1
            x = a1 * m2 * n2 + a2 * m1 * N1
            # There are infinitely many `x`. We want the one between
            # 0 and N1 - hence modulo
            N1 *= n2
            x = x % N1
            # In the next iteration, x becomes the coefficient of the folded term
            a1 = x
        # The last x is the result
        return a1
