#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict

e = Env(12)
e.T("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""", 10, 36)
e.T("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""", 19, 103)
e.T("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""", 226, 3509)


class RouteFinder:
    def __init__(self):
        self.adj = defaultdict(list)
    
    def add_edge(self, edge):
        start, end = edge.split('-')
        self.adj[start] += [end]
        self.adj[end] += [start]
    
    def _next_step(self, current, visited, double_small):
        if current == 'end':
            return 1
        first = current[0]
        major = first >= 'A' and first <= 'Z'
        if current in visited and not major:
            if not double_small and current != 'start':
                double_small.append(current)
            else:
                return 0
        if not major:
            visited.add(current)
        counter = 0
        for next in self.adj[current]:
            counter += self._next_step(next, visited, double_small)
        if not major:
            if double_small and double_small[0] == current:
                double_small.pop()
            else:
                visited.remove(current)
        return counter

    def count_all_from_start_to_end(self, small_twice=False):
        return self._next_step('start', set(), [] if small_twice else ['_'])


def part1(input):
    finder = RouteFinder()
    for ln in input.get_valid_lines():
        finder.add_edge(ln)
    return finder.count_all_from_start_to_end()


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    finder = RouteFinder()
    for ln in input.get_valid_lines():
        finder.add_edge(ln)
    return finder.count_all_from_start_to_end(True)


e.run_tests(2, part2)
e.run_main(2, part2)
