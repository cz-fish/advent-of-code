from typing import List

class Integers:
    @classmethod
    def prime_factors(cls, n: int) -> List[int]:
        """Returns a list of all prime factors of the given integer
           'n' in ascending order. Returns and empty list for integers
           lower than 2."""
        if n < 2:
            return []
        factors = []
        x = 2
        while x <= n:
            if n % x == 0:
                factors.append(x)
                n = n // x
            elif x == 2:
                x = 3
            else:
                x += 2
        return factors

    @classmethod
    def all_divisors(cls, n: int) -> List[int]:
        """Returns all integral divisors of a given integer 'n' in ascending
           order. Always returns at least the number 1."""
        primes = Integers.prime_factors(n)
        other_divisors = set([1])
        q1 = []
        for i in primes:
            q2 = []
            for x in q1:
                other_divisors.add(i * x)
                q2.append(i * x)
            q2.append(i)
            q1 += q2
        return sorted(list(set(primes).union(other_divisors)))

    @classmethod
    def gcd(cls, a: int, b: int) -> int:
        """Greatest common divisor of 'a' and 'b'"""
        A = max(a, b)
        B = min(a, b)
        while B != 0:
            x = A % B
            A = B
            B = x
        return A

    @classmethod
    def lcm(cls, a: int, b: int) -> int:
        """Least common multiple of 'a' and 'b'"""
        return a * b // Integers.gcd(a, b)
