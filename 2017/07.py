#!/usr/bin/python3.12

from pyaoc import Env
from dataclasses import dataclass

e = Env(7)
e.T("""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""", "tknk", 60)

@dataclass
class Prog:
    name: str
    weight: int
    sub: list[str]


def parse_progs(input):
    progs = {}
    for ln in input.get_valid_lines():
        parts = ln.split(' ', 2)
        name = parts[0]
        assert parts[1].startswith('(')
        assert parts[1].endswith(')')
        weight = int(parts[1][1:-1])
        subs = []
        if len(parts) > 2:
            assert parts[2].startswith('-> '), f"'{parts[2]}'"
            subs = parts[2][3:].split(', ')
        assert name not in progs
        progs[name] = Prog(name, weight, subs)
    return progs


def find_root(progs):
    subs = []
    for p in progs.values():
        subs.extend(p.sub)
    left = set(progs.keys())
    right = set(subs)
    bottom = left - right
    assert len(bottom) == 1
    return list(bottom)[0]


def part1(input):
    progs = parse_progs(input)
    return find_root(progs)


e.run_tests(1, part1)
e.run_main(1, part1)


def get_weight(progs, node, weights):
    if node in weights:
        return weights[node]
    w = progs[node].weight + sum([get_weight(progs, n, weights) for n in progs[node].sub])
    weights[node] = w
    return w


def balance(progs, rootname, weights):
    root = progs[rootname]
    sub_weights = []
    for s in root.sub:
        sub_weights.append(get_weight(progs, s, weights))
    if not sub_weights:
        return None
    max_w = max(sub_weights)
    if max_w == min(sub_weights):
        return None
    print(rootname, sub_weights)
    overweight = [i for i,s in enumerate(sub_weights) if s == max_w]
    assert len(overweight) == 1
    branch = root.sub[overweight[0]]
    b = balance(progs, branch, weights)
    if b is None:
        diff = max_w - min(sub_weights)
        b = progs[branch].weight - diff
        print(rootname, "calculated", b, "for branch", branch)
        return b
    else:
        print(rootname, "pass through", b)
        return b
        

def part2(input):
    progs = parse_progs(input)
    rootname = find_root(progs)
    weights = {}
    return balance(progs, rootname, weights)


e.run_tests(2, part2)
e.run_main(2, part2)

# 872 too low