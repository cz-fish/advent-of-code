#!/usr/bin/python3.12

from pyaoc import Env
from dataclasses import dataclass
import re

e = Env(20)
e.T("""p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>""", 0, None)
e.T("""p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>""", None, 1)


@dataclass
class V3:
    x: int
    y: int
    z: int
    def __repr__(self):
        return f"<{self.x},{self.y},{self.z}>"


@dataclass
class Particle:
    p: V3
    v: V3
    a: V3


rV3 = re.compile(r'(-?\d+),(-?\d+),(-?\d+)')
def parse_input(input):
    part = []
    for ln in input.get_valid_lines():
        m = rV3.findall(ln)
        assert len(m) == 3
        vals = [V3(x=int(a[0]), y=int(a[1]), z=int(a[2])) for a in m]
        part.append(Particle(p=vals[0], v=vals[1], a=vals[2]))
    return part


def part1(input):
    part = parse_input(input)
    closest = None
    drift = None
    for i, p in enumerate(part):
        s = abs(p.a.x) + abs(p.a.y) + abs(p.a.z)
        if drift is None or drift > s:
            drift = s
            closest = i
    return closest


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
