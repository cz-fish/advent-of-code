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


# --- Helpers ---

def parse_input(input):
    gr = input.get_groups()
    assert len(gr) == 2 and len(gr[0]) == 1

    polymer = gr[0][0]
    counts = Counter(polymer)

    rules = {}
    for rule in gr[1]:
        left, right = rule.split(' -> ')
        assert len(left) == 2 and len(right) == 1
        rules[left] = right
    return polymer, counts, rules


def merge(a, b):
    for k, v in a.items():
        if k not in b:
            b[k] = v
        else:
            b[k] += v
    return b


# --- Linked list approach ---
def make_polymer_llist(polymerstr):
    polymer = []
    for i, c in enumerate(polymerstr):
        polymer.append([c, None if i == 0 else i - 1, None if i == len(polymerstr)-1 else i+1])
    return polymer


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


# --- Tree approach ---
def count_between(a, b, rules, depth):
    ins = rules[a+b]
    if depth == 1:
        return [{ins: 1}]
    if ins == a or ins == b:
        # recursive case
        levels = count_between(ins, ins, rules, depth - 1)
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
        nlevels = [{ins: 1}]
        for d in range(1, depth):
            nlevels.append(merge({ins: 1}, merge(levelsL[d-1], levelsR[d-1])))
    return nlevels


def count_tree(polymer, counts, rules, depth):
    for i in range(len(polymer)-1):
        levels = count_between(polymer[i], polymer[i+1], rules, depth)
        merge(levels[-1], counts)
    return max(counts.values()) - min(counts.values())


# --- Dynamic programming approach ---
def build_up(rules, depth):
    subtrees = {}
    for d in range(1, depth + 1):
        for k, v in rules.items():
            if d == 1:
                subtrees[(k, d)] = {v: 1}
            else:
                left = k[0] + v
                right = v + k[1]
                subtrees[(k, d)] = merge(subtrees[(left, d - 1)], merge(subtrees[(right, d - 1)], {v: 1}))
    return subtrees


def expand(polymer, counts, subtrees, depth):
    for i in range(len(polymer)-1):
        subtree = subtrees[(polymer[i:i+2], depth)]
        merge(subtree, counts)
    return max(counts.values()) - min(counts.values())


# --- Main ---

def solve(polymer, counts, rules, depth):
    # LList - fine for pt1, slow for pt2
    #polymer = make_polymer_llist(polymerstr)
    #for step in range(10):
    #    insert(polymer, counts, rules)
    #return max(counts.values()) - min(counts.values())

    # Tree - fine for pt1, slow for pt2
    #return count_tree(polymerstr, counts, rules, 10)

    # DP - fine for both parts
    return expand(polymer, counts, build_up(rules, depth), depth)


def part1(input):
    polymerstr, counts, rules = parse_input(input)
    return solve(polymerstr, counts, rules, 10)


def part2(input):
    polymerstr, counts, rules = parse_input(input)
    return solve(polymerstr, counts, rules, 40)


e.run_tests(1, part1)
e.run_main(1, part1)
e.run_tests(2, part2)
e.run_main(2, part2)
