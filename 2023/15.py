#!/usr/bin/python3.8

from aoc import Env

e = Env(15)
e.T("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""", 1320, 145)

def hash_string(s):
    val = 0
    for c in s:
        asc = ord(c)
        val = ((val + asc) * 17) % 256
    return val


def part1(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    line = lines[0]
    parts = line.split(',')
    return sum([hash_string(s) for s in parts])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    line = lines[0]
    instructions = line.split(',')
    boxes = [{} for _ in range(256)]
    for instr in instructions:
        lens = None
        if '=' in instr:
            label, lens = instr.split('=')
            lens = int(lens)
        elif '-' in instr:
            label, _ = instr.split('-')
        else:
            assert False, f"Invalid instruction 'instr'"
        hash = hash_string(label)
        box = boxes[hash]
        if lens is not None:
            box[label] = lens
        else:
            if label in box:
                del box[label]
    total = 0
    for box_nr, box in enumerate(boxes):
        for pos, key in enumerate(box.keys()):
            lens = box[key]
            strength = (box_nr + 1) * (pos + 1) * lens
            total += strength
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
