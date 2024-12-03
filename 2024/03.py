#!/usr/bin/python3.12

from pyaoc import Env
import re

e = Env(3)
e.T("mul(44,46)", 2024, None)
e.T("mul(123,4)", 123*4, None)
e.T("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))", 161, None)
e.T("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))", 161, 48)
e.T("don't()mul(2,2)", 4, 0)


def part1(input):
    total = 0
    mul_re = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    for ln in input.get_valid_lines():
        muls = mul_re.findall(ln)
        for m in muls:
            total += int(m[0]) * int(m[1])
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    mul_re = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|(do\(\))|(don't\(\))")
    total = 0
    enabled = True
    for ln in input.get_valid_lines():
        muls = mul_re.findall(ln)
        for m in muls:
            if m[2] == "do()":
                enabled = True
            elif m[3] == "don't()":
                enabled = False
            else:
                if enabled:
                    total += int(m[0]) * int(m[1])
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
