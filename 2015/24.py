#!/usr/bin/python3.12

from pyaoc import Env
from collections import deque

e = Env(24)
e.T("""1
2
3
4
5
7
8
9
10
11""", 99, 44)


def findMainSets(items, tgt):
    q = deque([[]])
    while q:
        s = q.popleft()
        t = sum(s)
        for i in items:
            if len(s) > 0 and i >= s[-1]:
                continue
            if t+i > tgt:
                continue
            n = s[:] + [i]
            if t+i == tgt:
                yield n
            else:
                q.append(n)


def canSplitInTwo(items, tgt):
    for _ in findMainSets(items, tgt):
        return True
    return False


def canSplitInThree(items, tgt):
    for second in findMainSets(items, tgt):
        rest = [i for i in items if i not in second]
        for _ in findMainSets(rest, tgt):
            return True
    return False


def qe(subset):
    p = 1
    for v in subset:
        p *= v
    return p


def solve(items, tgt, groups):
    items.sort(reverse=True)
    best = None
    checkFn = canSplitInTwo if groups == 3 else canSplitInThree
    #print(items)
    # find main set using the biggest numbers
    for mainset in findMainSets(items, tgt):
        #print(mainset)
        if best is not None:
            if len(mainset) > len(best):
                return best
        # check that the rest can be split in 2 or 3
        rest = [i for i in items if i not in mainset]
        if not checkFn(rest, tgt):
            continue
        # tiebreakers
        if best is None or qe(best) > qe(mainset):
            best = mainset
    return best


def part1(input):
    items = input.get_all_ints()
    total = sum(items)
    assert total % 3 == 0, f"Total weight {total} not divisible by 3"
    best = solve(items, total // 3, 3)
    assert best is not None
    return qe(best)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    items = input.get_all_ints()
    total = sum(items)
    assert total % 4 == 0, f"Total weight {total} not divisible by 4"
    best = solve(items, total // 4, 4)
    assert best is not None
    return qe(best)


e.run_tests(2, part2)
e.run_main(2, part2)
