#!/usr/bin/python3.8

from aoc import Env
import re
from typing import Tuple

e = Env(16)

example = [
    "Before: [3, 2, 1, 1]",
    "9 2 1 2",
    "After:  [3, 2, 2, 1]"
]

class WristwatchComputer:
    def __init__(self):
        self.reg = [0, 0, 0, 0]
    
    @classmethod
    def all_instructions(cls):
        return [
            "addr", "addi",
            "mulr", "muli",
            "banr", "bani",
            "borr", "bori",
            "setr", "seti",
            "gtir", "gtri", "gtrr",
            "eqir", "eqri", "eqrr",
        ]

    def step(self, instruction: Tuple[str, int, int, int]):
        op, s1, s2, dst = instruction

        first = self.reg[s1]
        if op[3] == 'i':
            second = s2
        elif op[3] == 'r':
            second = self.reg[s2]

        val = None
        if op[0] == 'a':
            val = first + second
        elif op[0] == 'm':
            val = first * second
        elif op[0] == 'b':
            if op[1] == 'a':
                val = first & second
            elif op[1] == 'o':
                val = first | second
        elif op[0] == 's':
            if op[3] == 'i':
                first = s1
            val = first
        elif op[0] in 'eg':
            if op[2] == 'i':
                first = s1
            if op[0] == 'g':
                val = 1 if first > second else 0
            else:
                val = 1 if first == second else 0
        else:
            assert False, f"Invalid opcode {op}, instruction {instruction}"
        
        if val is None:
            assert False, f"Invalid instruction {instruction}"

        self.reg[dst] = val


def parse_observed(group):
    assert len(group) == 3, f"{len(group)}: '{group}'"
    assert group[0].startswith("Before: ")
    assert group[2].startswith("After: ")
    r = re.compile(r'\d+')
    all_nums = lambda ln: tuple([int(x) for x in r.findall(ln)])
    return (
        all_nums(group[0]),
        all_nums(group[1]),
        all_nums(group[2])
    )


def parse_input(input):
    groups = [gr for gr in input.get_groups() if gr]
    assert len(groups) >= 2
    observed = []
    for i in range(len(groups) - 1):
        observed.append(parse_observed(groups[i]))
    return observed, groups[-1]


def num_opcodes(observed):
    before, instr, after = observed
    num = 0
    for opcode in WristwatchComputer.all_instructions():
        comp = WristwatchComputer()
        comp.reg = list(before)
        comp.step((opcode, instr[1], instr[2], instr[3]))
        if comp.reg == list(after):
            num += 1
    return num


def part1(input):
    observed, program = parse_input(input)
    # print(f"Total groups: {len(observed)}")
    return sum([1 for o in observed if num_opcodes(o) >= 3])


# == Tests ==
def test_parse_observed():
    expected = ((3, 2, 1, 1), (9, 2, 1, 2), (3, 2, 2, 1))
    actual = parse_observed(example)
    assert actual == expected, f"Fail: expected {expected}, actual {actual}"

def test_possible_opcodes():
    expected = 3
    actual = num_opcodes(parse_observed(example))
    assert actual == expected, f"Fail: expected {expected}, actual {actual}"


test_parse_observed()
test_possible_opcodes()
print("Tests passed")

e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)

