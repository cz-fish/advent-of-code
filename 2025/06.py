#!/usr/bin/python3.12

from pyaoc import Env
import re

e = Env(6, raw_lines=True)
e.T("""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """, 4277556, 3263827)


def parse_input(input):
    mat = []
    ops = None
    r = re.compile(r'[0-9*+]+')
    for ln in input.get_valid_lines():
        cols = r.findall(ln)
        assert len(cols) > 0
        if mat:
            assert len(mat[0]) == len(cols)
        if cols[0] in '*+':
            assert ops is None
            ops = cols
        else:
            mat.append([int(x) for x in cols])
    return mat, ops


def part1(input):
    mat, ops = parse_input(input)
    total = 0
    for i in range(len(ops)):
        op = ops[i]
        val = 0 if op == '+' else 1
        for row in mat:
            if op == '+':
                val += row[i]
            else:
                val *= row[i]
        total += val
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    assert len(lines) >= 2
    # all lines same length
    assert all([len(l) == len(lines[0]) for l in lines])
    total = 0
    current = []
    # right to left
    for idx in range(len(lines[0])-1, -1, -1):
        col = ''.join([lines[r][idx] for r in range(len(lines))])
        if not col.strip():
            # empty column
            assert not current
            continue
        op = col[-1]
        if op in '+*':
            # operator column
            current.append(int(col[:-1]))
            val = 0 if op == '+' else 1
            for x in current:
                if op == '+':
                    val += x
                else:
                    val *= x
            total += val
            current = []
        else:
            # number column
            current.append(int(col))
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
