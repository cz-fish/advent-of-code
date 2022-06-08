#!/usr/bin/python3.8

from aoc import Env
import re
from typing import Dict, List, Tuple
from wristwatch import WristwatchComputer

e = Env(16)

example = [
    "Before: [3, 2, 1, 1]",
    "9 2 1 2",
    "After:  [3, 2, 2, 1]"
]


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
    program = []
    for ln in groups[-1]:
        program.append(tuple([int(x) for x in ln.split(' ')]))
    return observed, program


def which_opcodes(observed):
    before, instr, after = observed
    possible = []
    for opcode in WristwatchComputer.all_instructions():
        comp = WristwatchComputer()
        comp.reg = list(before)
        comp.step((opcode, instr[1], instr[2], instr[3]))
        if comp.reg == list(after):
            possible.append(opcode)
    return possible


def part1(input):
    observed, program = parse_input(input)
    # print(f"Total groups: {len(observed)}")
    return sum([1 for o in observed if len(which_opcodes(o)) >= 3])


# == Tests ==
def test_parse_observed():
    expected = ((3, 2, 1, 1), (9, 2, 1, 2), (3, 2, 2, 1))
    actual = parse_observed(example)
    assert actual == expected, f"Fail: expected {expected}, actual {actual}"

def test_possible_opcodes():
    expected = 3
    actual = len(which_opcodes(parse_observed(example)))
    assert actual == expected, f"Fail: expected {expected}, actual {actual}"


test_parse_observed()
test_possible_opcodes()
print("Tests passed")

e.run_tests(1, part1)
e.run_main(1, part1)


def map_instruction_numbers(observed):
    all_ops = WristwatchComputer.all_instructions()
    mapping = {i: None for i in range(len(all_ops))}
    undecided = set([x for x in all_ops])
    possible = {}
    for o in observed:
        opnum = o[1][0]
        if mapping[opnum] is not None:
            # this opnum is already assigned to an opcode
            continue
        alter = set([a for a in which_opcodes(o) if a in undecided])
        if opnum in possible:
            alter = alter.intersection(possible[opnum])
        assert len(alter) > 0
        if len(alter) == 1:
            mapping[opnum] = alter.pop()
            undecided.remove(mapping[opnum])
        else:
            possible[opnum] = alter
    assert None not in mapping.values()
    return mapping


def part2(input):
    observed, program = parse_input(input)
    mapping = map_instruction_numbers(observed)
    for k, v in mapping.items():
        print(f"{k} -> {v}")
    comp = WristwatchComputer()
    comp.run(program, mapping)
    return comp.reg[0]


e.run_main(2, part2)

