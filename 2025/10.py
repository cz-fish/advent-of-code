#!/usr/bin/python3.12

from pyaoc import Env
from collections import deque
import re

e = Env(10)
e.T("""[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""", 7, 33)


r_mach = re.compile(r'^\[(?P<target>[.#]+)\] (?P<buttons>.*) \{(?P<joltage>.*)\}')


def parse_machine(line):
    m = r_mach.match(line)
    assert m is not None
    target = m["target"]
    button_str = m["buttons"].split(" ")
    buttons = []
    for bstr in button_str:
        effects = [int(x) for x in bstr[1:-1].split(',')]
        buttons.append(effects)
    joltages = [int(x) for x in m["joltage"].split(',')]
    return target, buttons, joltages


def flip(lights, indexes):
    for i in indexes:
        lights ^= 2 ** i
    return lights


def min_light_presses(target_str, buttons):
    shift = 1
    target = 0
    for c in target_str:
        if c == '#':
            target += shift
        shift *= 2
    visited = set()
    visited.add(0)
    q = deque()
    q.append((0, 0))
    while q:
        depth, lights = q.popleft()
        if lights == target:
            return depth
        for but in buttons:
            new_lights = flip(lights, but)
            if new_lights not in visited:
                q.append((depth + 1, new_lights))
                visited.add(new_lights)
    else:
        assert False, f"solution not found for target {target}"


def part1(input):
    total = 0
    for ln in input.get_valid_lines():
        target, buttons, _ = parse_machine(ln)
        total += min_light_presses(target, buttons)
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def increment(counters, button):
    return tuple([counters[i] + (1 if i in button else 0) for i in range(len(counters))])


def over(counters, target):
    for i in range(len(counters)):
        if counters[i] > target[i]:
            return True
    return False


def min_joltage_presses_slow1(target_lst, buttons):
    target = tuple(target_lst)
    size = len(target)
    cntrs = tuple([0] * size)
    visited = set()
    visited.add(cntrs)
    q = deque()
    q.append((0, cntrs))
    while q:
        depth, cntrs = q.popleft()
        if cntrs == target:
            return depth
        for but in buttons:
            new_cntrs = increment(cntrs, but)
            if new_cntrs not in visited and not over(cntrs, target):
                q.append((depth + 1, new_cntrs))
                visited.add(new_cntrs)
    else:
        assert False, f"solution not found for target {target}"


def min_joltage_presses_slow2(target_lst, buttons):
    # Most impactful buttons first
    buttons.sort(key=lambda b: len(b), reverse=True)
    def next_button(index, presses, remain, remain_sum):
        nonlocal buttons
        current_btn_limit = min(remain[i] for i in buttons[index])
        if current_btn_limit * len(buttons[index]) == remain_sum:
            # target reached exactly
            return presses + current_btn_limit
        if index == len(buttons) - 1:
            # no more buttons
            return None
        for i in buttons[index]:
            remain[i] -= current_btn_limit
            remain_sum -= current_btn_limit
        for pushes in range(current_btn_limit, -1, -1):
            val = next_button(index + 1, presses + pushes, remain, remain_sum)
            if val is not None:
                return val
            for i in buttons[index]:
                remain[i] += 1
                remain_sum += 1
        return None
    return next_button(0, 0, target_lst, sum(target_lst))

# target[0] = x0 * button[0]0 + x1 * button[1]0 + ...
# target[1] = x0 * button[0]1 + x1 * button[1]0 + ...
# target[2] = x0 * button[0]2 + x1 * button[1]0 + ...
# not a unique solution; there could be many different solutions,
# and we need to find the one with the smallest sum over X
# ...
# index 0 on buttons 1, 3, 4
# joltage[0] = P[1] + P[3] + P[4]
# index 1 in buttons 2, 3, 5, 6
# joltage[1] = P[2] + P[3] + P[5] + P[6]

import scipy.optimize

def min_joltage_presses_c(target_lst, buttons):
    A = [[1 if i in buttons[j] else 0 for j in range(len(buttons))] for i in range(len(target_lst))]
    B = target_lst
    X = scipy.optimize.linprog([1] * len (buttons), A_eq=A, b_eq=B, integrality=1)
    #print(X)
    assert X.success
    return int(X.fun)


def part2(input):
    total = 0
    for i, ln in enumerate(input.get_valid_lines()):
        _, buttons, joltages = parse_machine(ln)
        presses = min_joltage_presses_c(joltages, buttons)
        #print(f"machine {i + 1}, presses {presses}")
        total += presses
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
