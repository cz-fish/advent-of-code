#!/usr/bin/python3.8

from pyaoc import Env
from collections import namedtuple, defaultdict
import re

e = Env(3)
e.T("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""", 4, 3)


Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])


def parse_input(input):
    claims = []
    for ln in input.get_valid_lines():
        m = re.search(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', ln)
        assert m is not None
        id, left, top, wid, hei = [int(m.group(i)) for i in range(1, 6)]
        claims += [Claim(id=id, left=left, top=top, width=wid, height=hei)]
    return claims


def draw_claims(claims):
    fabric = defaultdict(int)
    for claim in claims:
        for x in range(claim.left, claim.left + claim.width):
            for y in range(claim.top, claim.top + claim.height):
                fabric[(x, y)] += 1
    return fabric


def part1(input):
    claims = parse_input(input)
    fabric = draw_claims(claims)
    overlaps = len([0 for _, v in fabric.items() if v > 1])
    return overlaps


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    claims = parse_input(input)
    fabric = draw_claims(claims)
    for claim in claims:
        good = True
        for x in range(claim.left, claim.left + claim.width):
            if not good:
                break
            for y in range(claim.top, claim.top + claim.height):
                if fabric[(x, y)] > 1:
                    good = False
                    break
        if good:
            return claim.id


e.run_tests(2, part2)
e.run_main(2, part2)
