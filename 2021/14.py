#!/usr/bin/python3.8

from aoc import Env
from collections import Counter

e = Env(14)
e.T("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""", 1588, 2188189693529)


def parse_input(input):
    gr = input.get_groups()
    assert len(gr) == 2 and len(gr[0]) == 1

    polymerstr = gr[0][0]
    counts = Counter(polymerstr)
    polymer = []
    for i, c in enumerate(polymerstr):
        polymer.append([c, None if i == 0 else i - 1, None if i == len(polymerstr)-1 else i+1])

    rules = {}
    for rule in gr[1]:
        left, right = rule.split(' -> ')
        assert len(left) == 2 and len(right) == 1
        rules[left] = right
    return polymer, counts, rules


def insert(polymer, counts, rules):
    ptr = 0
    while True:
        first, prev, next = polymer[ptr]
        if next is None:
            break
        second = polymer[next][0]
        pair = first + second
        if pair in rules:
            ins = rules[pair]
            index = len(polymer)
            polymer.append([ins, ptr, next])
            polymer[ptr][2] = index
            polymer[next][1] = index
            counts[ins] += 1
        ptr = next


def part1(input):
    polymer, counts, rules = parse_input(input)
    for step in range(10):
        insert(polymer, counts, rules)
    return max(counts.values()) - min(counts.values())


e.run_tests(1, part1)
e.run_main(1, part1)


def merge(a, b):
    for k, v in a.items():
        if k not in b:
            b[k] = v
        else:
            b[k] += v
    return b


def count_between(a, b, rules, depth):
    ins = rules[a+b]
    if depth == 1:
        return [{ins: 1}]
    if ins == a or ins == b:
        # recursive case
        levels = count_between(ins, ins, rules, depth - 1)
        #print("subtree", levels)
        nlevels = [{ins: 1}]
        for d in range(1, depth):
            nl = {ins: d+1}
            for x in range(d):
                merge(levels[x], nl)
            nlevels.append(nl)
    else:
        # non recursive case
        levelsL = count_between(a, ins, rules, depth - 1)
        levelsR = count_between(ins, b, rules, depth - 1)
        #print(levelsL, levelsR)
        nlevels = [{ins: 1}]
        for d in range(1, depth):
            nlevels.append(merge({ins: 1}, merge(levelsL[d-1], levelsR[d-1])))
    #print(f'[{depth}] between {a} {b}: {nlevels}')
    return nlevels

#    counts[ins] += 1
#    if depth > 1:
#        count_between(a, ins, counts, rules, depth - 1)
#        count_between(ins, b, counts, rules, depth - 1)


def count(polymer, rules, depth):
    counts = Counter(polymer)
    for i in range(len(polymer)-1):
        levels = count_between(polymer[i], polymer[i+1], rules, depth)
        merge(levels[-1], counts)
    print(f"depth {depth} length {sum(counts.values())}: {counts}")
    return max(counts.values()) - min(counts.values())

"""
Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

>>> Counter('NCNBCHB')
Counter({'N': 2, 'C': 2, 'B': 2, 'H': 1})
>>> Counter('NBCCNBBBCBHCB')
Counter({'B': 6, 'C': 4, 'N': 2, 'H': 1})
>>> Counter('NBBBCNCCNBBNBNBBCHBHHBCHB')
Counter({'B': 11, 'N': 5, 'C': 5, 'H': 4})
>>> Counter('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
Counter({'B': 23, 'N': 11, 'C': 10, 'H': 5})
"""

def build_up(rules, depth):
    subtrees = {}
    for d in range(1, depth+1):
        for k, v in rules.items():
            if d == 1:
                subtrees[(k, d)] = {v: 1}
            else:
                left = k[0] + v
                right = v + k[1]
                subtrees[(k, d)] = merge(subtrees[(left, d-1)], merge(subtrees[(right, d-1)], {v: 1}))
    return subtrees


def expand(polymer, subtrees, depth):
    counts = Counter(polymer)
    for i in range(len(polymer)-1):
        subtree = subtrees[(polymer[i:i+2], depth)]
        merge(subtree, counts)
    return counts


def part2(input):
    gr = input.get_groups()
    assert len(gr) == 2 and len(gr[0]) == 1
    polymer = gr[0][0]
    rules = {}
    for rule in gr[1]:
        left, right = rule.split(' -> ')
        assert len(left) == 2 and len(right) == 1
        rules[left] = right

    subtrees = build_up(rules, 40)
    print(3, expand(polymer, subtrees, 3))
    print(10, expand(polymer, subtrees, 10))
    counts = expand(polymer, subtrees, 40)
    print(40, counts)
    return max(counts.values()) - min(counts.values())


    #print(count(polymer, rules, 1))
    #print(count(polymer, rules, 2))
    print(count(polymer, rules, 3))
    print(count(polymer, rules, 10))
    print(count(polymer, rules, 40))
    return count(polymer, rules, 40)


e.run_tests(2, part2)
e.run_main(2, part2)
