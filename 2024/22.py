#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict

e = Env(22)
e.T("""1
10
100
2024""", 37327623, None)
e.T("""1
2
3
2024""", None, 23)


def next_random(n):
    n = (n ^ (n * 64)) % 16777216
    n = (n ^ (n // 32)) % 16777216
    n = (n ^ (n * 2048)) % 16777216
    return n


def part1(input):
    nums = input.get_ints()
    total = 0
    for n in nums:
        for i in range(2000):
            n = next_random(n)
        total += n
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def count_bananas(n, counter):
    prev_digit = n % 10
    seq_seen = set()
    n_seen = set()
    seq = []
    for i in range(2000):
        n = next_random(n)
        if n in n_seen:
            break
        digit = n % 10
        diff = digit - prev_digit
        prev_digit = digit
        if len(seq) < 3:
            seq.append(diff)
        else:
            n_seen.add(n)
            if len(seq) == 3:
                seq = (seq[0], seq[1], seq[2], diff)
            else:
                seq = (seq[1], seq[2], seq[3], diff)
            if seq not in seq_seen:
                seq_seen.add(seq)
                counter[seq] += digit


def part2(input):
    nums = input.get_ints()
    bananas = defaultdict(int)
    for num in nums:
        count_bananas(num, bananas)
    seq = list(bananas.items())
    seq.sort(key=lambda x: -x[1])
    best_seq, max_bananas = seq[0]
    #print(best_seq, max_bananas)
    return max_bananas


e.run_tests(2, part2)
e.run_main(2, part2)
