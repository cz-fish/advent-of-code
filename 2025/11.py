#!/usr/bin/python3.12

from pyaoc import Env
from collections import deque, defaultdict

e = Env(11)
e.T("""aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out""", 5, None)
e.T("""svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""", None, 2)


def parse_input(input):
    adj = {}
    for ln in input.get_valid_lines():
        left, right = ln.split(": ")
        dests = right.split(" ")
        assert left not in adj
        assert len(left) == 3
        assert all([len(x) == 3 for x in dests])
        adj[left] = dests
    return adj


def count_paths(graph, start, end):
    paths = 0
    q = deque()
    q.append((start, [start]))
    while q:
        w, path = q.popleft()
        if w == end:
            paths += 1
            continue
        if w not in graph:
            continue
        for n in graph[w]:
            if n in path:
                continue
            q.append((n, path + [n]))
    return paths


def part1(input):
    graph = parse_input(input)
    return count_paths(graph, "you", "out")


e.run_tests(1, part1)
e.run_main(1, part1)


def count_paths2(graph, start, end):
    memo = {}
    def steps_inner(current):
        nonlocal memo
        if current == end:
            return 1
        if current not in memo:
            if current not in graph:
                memo[current] = 0
            else:
                memo[current] = sum([steps_inner(n) for n in graph[current]])
        return memo[current]
    return steps_inner(start)


def part2(input):
    # svr -> out through fft and dac
    graph = parse_input(input)
    # This assumes that dac is not accidentally visited on the
    # way from svr to fft, and vice versa
    svr_fft = count_paths2(graph, "svr", "fft")
    fft_dac = count_paths2(graph, "fft", "dac")
    dac_out = count_paths2(graph, "dac", "out")
    svr_dac = count_paths2(graph, "svr", "dac")
    dac_fft = count_paths2(graph, "dac", "fft")
    fft_out = count_paths2(graph, "fft", "out")
    return svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out


e.run_tests(2, part2)
e.run_main(2, part2)
