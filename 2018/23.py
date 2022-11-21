#!/usr/bin/python3.8

from aoc import Env
from dataclasses import dataclass
import heapq
import re

e = Env(23)
e.T("""pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""", 7, None)
e.T("""pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""", None, 36)

numbers = re.compile(r'-?\d+')

@dataclass
class Nanobot:
    x: int
    y: int
    z: int
    r: int

    @classmethod
    def make(cls, line):
        m = numbers.findall(line)
        assert m, f"line cannot be parsed '{line}'"
        nums = [int(x) for x in m]
        assert len(nums) == 4, f"line doesn't have 4 numbers '{line}', {m}"
        return Nanobot(x=nums[0], y=nums[1], z=nums[2], r=nums[3])

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
    
    def in_range(self, other):
        return self.dist(other) <= self.r
    
    def overlaps(self, other):
        return self.dist(other) <= self.r + other.r


def part1(input):
    bots = []
    biggest = (0, None)
    for line in input.get_valid_lines():
        bots.append(Nanobot.make(line))
        if bots[-1].r > biggest[0]:
            biggest = (bots[-1].r, len(bots) - 1)

    assert biggest[1] is not None
    captain = bots[biggest[1]]
    count_in_range = sum([1 for bot in bots if captain.in_range(bot)])
    return count_in_range


e.run_tests(1, part1)
e.run_main(1, part1)


class Quad:
    def __init__(self, limits, bots):
        self.limits = limits
        self.ranges = [lim[1] - lim[0] + 1 for lim in limits]
        self.size = self.ranges[0] * self.ranges[1] * self.ranges[2]
        self.dist = self._dist2point(0, 0, 0)
        self.num = sum([1 for b in bots if self._dist2point(b.x, b.y, b.z) <= b.r])

    def _dist2point(self, x, y, z):
        # shortest distance from the quad to the given point
        def clamp(v, lower, upper):
            return min(upper, max(lower, v))
        # cell of the quad that is closest to the point
        closest = [
            clamp(x, self.limits[0][0], self.limits[0][1]),
            clamp(y, self.limits[1][0], self.limits[1][1]),
            clamp(z, self.limits[2][0], self.limits[2][1]),
        ]
        return abs(x - closest[0]) + abs(y - closest[1]) + abs(z - closest[2])

    def subdivide(self, bots):
        lcut = [
            self.limits[i][0] + self.ranges[i] // 2 - 1 for i in range(len(self.limits))
        ]
        mins = [lim[0] for lim in self.limits]
        maxs = [lim[1] for lim in self.limits]
        rcut = [cut + 1 for cut in lcut]
        yield Quad([[mins[0], lcut[0]], [mins[1], lcut[1]], [mins[2], lcut[2]]], bots)
        yield Quad([[rcut[0], maxs[0]], [mins[1], lcut[1]], [mins[2], lcut[2]]], bots)
        yield Quad([[mins[0], lcut[0]], [rcut[1], maxs[1]], [mins[2], lcut[2]]], bots)
        yield Quad([[rcut[0], maxs[0]], [rcut[1], maxs[1]], [mins[2], lcut[2]]], bots)
        yield Quad([[mins[0], lcut[0]], [mins[1], lcut[1]], [rcut[2], maxs[2]]], bots)
        yield Quad([[rcut[0], maxs[0]], [mins[1], lcut[1]], [rcut[2], maxs[2]]], bots)
        yield Quad([[mins[0], lcut[0]], [rcut[1], maxs[1]], [rcut[2], maxs[2]]], bots)
        yield Quad([[rcut[0], maxs[0]], [rcut[1], maxs[1]], [rcut[2], maxs[2]]], bots)
    
    def __lt__(self, other):
        return (-self.num, self.dist, self.size) < (-other.num, other.dist, other.size)

    def __repr__(self):
        return f"Quad[limits={self.limits}, ranges={self.ranges}, size={self.size}, dist={self.dist}, num={self.num}]"


def part2(input):
    bots = [Nanobot.make(line) for line in input.get_valid_lines()]
    limits = [
        (min([b.x - b.r for b in bots]), max([b.x + b.r for b in bots])),
        (min([b.y - b.r for b in bots]), max([b.y + b.r for b in bots])),
        (min([b.z - b.r for b in bots]), max([b.z + b.r for b in bots])),
    ]
    quads = []
    # Heap of quads to be sorted by
    # 1) number of bots in range (highest first)
    # 2) distance to origin (shortest first)
    # 3) size of the quad (smallest first)
    # (see Quad.__lt__)
    counter = 0
    heapq.heappush(quads, Quad(limits, bots))
    while(quads):
        quad = heapq.heappop(quads)
        counter += 1
        if quad.size == 1:
            # This is a single cell. Because of the sorting order of the
            # heap, this quad is the solution
            print(f"After {counter} iterations")
            return quad.dist
        # Subdivide into 8 more quads
        for subquad in quad.subdivide(bots):
            if subquad.size > 0 and subquad.num > 0:
                heapq.heappush(quads, subquad)
    assert False, "solution not found!"


e.run_tests(2, part2)
e.run_main(2, part2)
