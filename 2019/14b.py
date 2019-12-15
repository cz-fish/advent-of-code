#!/usr/bin/python3.8

from collections import defaultdict
import sys

def parse_element(comp):
    p = comp.strip().split(' ')
    return p[1], int(p[0])

def parse_reaction(line):
    source, prod = line.split('=>')
    comps = source.split(', ')
    return (parse_element(prod), [parse_element(c) for c in comps])

react_map = {}
with open('input14.txt', 'rt') as f:
    for reaction in f.readlines():
        prod, sources = parse_reaction(reaction.strip())
        print(prod[0], prod[1], sources)
        react_map[prod[0]] = (prod[1], sources)

have = defaultdict(int)
need = defaultdict(int)
per_unit = defaultdict(int)
need['FUEL'] = 1
ore = 0

while need:
    comp = list(need.keys())[0]
    howmuch = need[comp]
    del need[comp]
    number, sources = react_map[comp]
    while howmuch > 0:
        for key, amount in sources:
            per_unit[key] += amount
            if key == 'ORE':
                ore += amount
            else:
                h = min(have[key], amount)
                r = amount - h
                have[key] -= h
                need[key] += r
        howmuch -= number
        extra = max(0, -howmuch)
        if extra > 0:
            have[comp] += extra

ore_per_unit = ore
ore_left = 1000000000000
print("ore-per-1-fuel", ore_per_unit)
produced = trillion // ore_per_unit
print("produced", produced)
ore_left = ore_left - produced * ore_per_unit
print("remaining ore", ore_left)
print("overproduce")
for k, v in have.items():
    if v > 0:
        print(k, v, v*produced)

