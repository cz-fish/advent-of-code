#!/usr/bin/python3.12

from pyaoc import Env
from collections import deque

e = Env(12)
e.T("""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""", 6, 2)


def parse_adjacency(input):
    adj = {}
    for ln in input.get_valid_lines():
        left, right = ln.split(" <-> ")
        con = [int(x) for x in right.split(", ")]
        adj[int(left)] = con
    return adj


def component_size(adj, start):
    group = set()
    q = deque([start])
    while q:
        node = q.popleft()
        if node in group:
            continue
        group.add(node)
        for n in adj[node]:
            if n not in group:
                q.append(n)
    return len(group)


def part1(input):
    adj = parse_adjacency(input)
    return component_size(adj, 0)


e.run_tests(1, part1)
e.run_main(1, part1)


def count_components(adj):
    used = set()
    components = 0
    for start in adj.keys():
        if start in used:
            continue
        components += 1
        q = deque([start])
        while q:
            node = q.popleft()
            if node in used:
                continue
            used.add(node)
            for n in adj[node]:
                if n not in used:
                    q.append(n)
    return components


def part2(input):
    adj = parse_adjacency(input)
    return count_components(adj)


e.run_tests(2, part2)
e.run_main(2, part2)
