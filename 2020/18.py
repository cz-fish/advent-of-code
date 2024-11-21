#!/usr/bin/python3.8

from pyaoc import Env
import re

e = Env(18)
e.T("1 + 2 * 3 + 4 * 5 + 6", 71, 231)
e.T("1 + (2 * 3) + (4 * (5 + 6))", 51, 51)
e.T("2 * 3 + (4 * 5)", None, 46)
e.T("5 + (8 * 3 + 9 + 3 * 4 * 3)", None, 1445)
e.T("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", None, 669060)
e.T("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", None, 23340)


def evaluate_expr(ln):
    tokens = re.findall(r'(\d+|\+|\*|\(|\))', ln)
    stack = []
    for tok in tokens:
        if tok in '(+*':
            stack.append(tok)
            continue
        elif tok == ')':
            # assuming that parentheses are never empty
            val = stack.pop()
            _ = stack.pop()
        else:
            val = int(tok)

        if not stack or stack[-1] == '(':
            stack.append(val)
        else:
            op = stack.pop()
            acc = stack.pop()
            val = {'+': val + acc, '*': val * acc}[op]
            stack.append(val)
    return stack[-1]


class A:
    def __init__(self, v):
        self.v = v

    def __int__(self):
        return self.v

    def __add__(self, other):
        return A(self.v * other.v)

    def __mul__(self, other):
        return A(self.v + other.v)


def evaluate_expr2(ln):
    ex = re.sub(r'(\d+)', r'A(\1)', ln).replace('+', '-').replace('*', '+').replace('-', '*')
    return int(eval(ex))


def part1(input):
    return sum([evaluate_expr(ln) for ln in input.get_valid_lines()])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return sum([evaluate_expr2(ln) for ln in input.get_valid_lines()])


e.run_tests(2, part2)
e.run_main(2, part2)
