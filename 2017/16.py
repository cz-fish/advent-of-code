#!/usr/bin/python3.12

from pyaoc import Env

e = Env(16, param=16)
e.T("""s1,x3/4,pe/b""", "baedc", None, param=5)


"""
Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.
"""


def one_pass(progs, ops):
    for op in ops:
        if op[0] == 's':
            amount = int(op[1:])
            progs = progs[-amount:] + progs[:-amount]
        elif op[0] == 'x':
            i1, i2 = [int(x) for x in op[1:].split('/')]
            progs[i1], progs[i2] = progs[i2], progs[i1]
        elif op[0] == 'p':
            c1, c2 = [x for x in op[1:].split('/')]
            i1 = progs.index(c1)
            i2 = progs.index(c2)
            progs[i1], progs[i2] = progs[i2], progs[i1]
    return progs


def part1(input):
    num_progs = e.get_param()
    line = input.get_lines()[0]
    ops = line.split(',')
    progs = [chr(i + ord('a')) for i in range(num_progs)]
    progs = one_pass(progs, ops)
    return ''.join(progs)


e.run_tests(1, part1)
e.run_main(1, part1)


def find_period(num_progs, ops):
    # Assumption: after a certain number of repetitions of the dance,
    # the programs will again be in the starting order.
    # It is not guaranteed to be < 1bil, as there are up to 16! different
    # permutations; but if we're lucky and there happens to be a period
    # then that will reduce the number of repetitions of the dance
    # from 1bil to size of the period
    progs = [chr(i + ord('a')) for i in range(num_progs)]
    seen = {}
    inv_map = {}
    target = ''.join(progs)
    retries = 100
    for it in range(retries):
        s = ''.join(progs)
        if s in seen:
            assert s == target, "Repetition found, but it's not the original configuration"
            print(f"Repeat '{s}', before {seen[s]}, now {it}, period {it - seen[s]}")
            return it - seen[s], inv_map
        seen[s] = it
        inv_map[it] = s
        progs = one_pass(progs, ops)
    assert False, f"Repetition period not found in {retries} retries"


def part2(input):
    num_progs = e.get_param()
    line = input.get_lines()[0]
    ops = line.split(',')
    period, inv_map = find_period(num_progs, ops)
    index = 1000000000 % period
    return inv_map[index]


e.run_tests(2, part2)
e.run_main(2, part2)
