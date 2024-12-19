#!/usr/bin/python3.12

from pyaoc import Env
from collections import deque

e = Env(19)
e.T("""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""", 6, 16)


class Trie:
    def __init__(self):
        self.root = {}

    def add_word(self, word):
        node = self.root
        for pos, c in enumerate(word):
            if c not in node:
                node[c] = {}
            node = node[c]
        node['.'] = True

    def is_possible(self, pattern):
        assert '.' not in self.root
        resets = set([0])
        q = deque()
        q.append((0, self.root))
        while q:
            pos, node = q.popleft()
            if pos == len(pattern):
                if '.' in node:
                    return True
                continue
            if '.' in node and pos not in resets:
                resets.add(pos)
                q.append((pos, self.root))
            c = pattern[pos]
            if c in node:
                q.append((pos + 1, node[c]))
        return False

    def count_ways(self, pattern, spos, cache):
        q = deque()
        q.append((spos, self.root))
        ways = 0
        while q:
            pos, node = q.popleft()
            if pos == len(pattern):
                if '.' in node:
                    ways += 1
                continue
            if '.' in node:
                if pos not in cache:
                    self.count_ways(pattern, pos, cache)
                ways += cache[pos]
            c = pattern[pos]
            if c in node:
                q.append((pos + 1, node[c]))
        cache[spos] = ways
        return ways


def build_trie(towels):
    trie = Trie()
    for towel in towels:
        trie.add_word(towel)
    return trie


def part1(input):
    towel_line, patterns = input.get_groups()
    towels = towel_line[0].split(', ')
    trie = build_trie(towels)
    return sum([1 for pattern in patterns if trie.is_possible(pattern)])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    towel_line, patterns = input.get_groups()
    towels = towel_line[0].split(', ')
    trie = build_trie(towels)
    #total = 0
    #for i, pattern in enumerate(patterns):
    #    w = trie.count_ways(pattern, 0, {})
    #    print(f"Pattern {i+1}: {pattern} -> {w}")
    #    total += w
    #return total
    return sum([trie.count_ways(pattern) for pattern in patterns])


e.run_tests(2, part2)
e.run_main(2, part2)
