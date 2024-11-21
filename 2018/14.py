#!/usr/bin/python3.8

from pyaoc import Env

e = Env(14)
e.T("9", "5158916779", None)
e.T("5", "0124515891", None)
e.T("18", "9251071085", None)
e.T("2018", "5941429882", None)
e.T("51589", None, 9)
e.T("01245", None, 5)
e.T("92510", None, 18)
e.T("59414", None, 2018)

SEED = [3, 7]


def do_iterations(n):
    scores = SEED[:]
    p1 = 0
    p2 = 1
    while len(scores) < n + 10:
        v = scores[p1] + scores[p2]
        if v >= 10:
            scores.append(v // 10)
        scores.append(v % 10)
        p1 = (p1 + 1 + scores[p1]) % len(scores)
        p2 = (p2 + 1 + scores[p2]) % len(scores)
    return scores


def part1(input):
    n = input.get_all_ints()[0]
    scores = do_iterations(n)
    return ''.join([str(x) for x in scores[n:n+10]])


e.run_tests(1, part1)
e.run_main(1, part1)


def find_target(target: str):
    scores = SEED[:]
    p1 = 0
    p2 = 1
    tail = ''.join([str(x) for x in scores])
    assert len(tail) < len(target)

    def is_good_tail(digit):
        nonlocal tail
        nonlocal scores
        scores.append(digit)
        tail += str(digit)
        return tail.endswith(target)

    counter = 0
    while True:
        v = scores[p1] + scores[p2]
        if v >= 10:
            if is_good_tail(v // 10):
                return len(scores) - len(target)
        if is_good_tail(v % 10):
            return len(scores) - len(target)
        p1 = (p1 + 1 + scores[p1]) % len(scores)
        p2 = (p2 + 1 + scores[p2]) % len(scores)
        counter += 1
        if counter % 1000000 == 0:
            print(f"Still going after {counter} iterations")


def part2(input):
    target = input.get_valid_lines()[0]
    n = find_target(target)
    return n


e.run_tests(2, part2)
e.run_main(2, part2)
