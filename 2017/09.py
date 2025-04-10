#!/usr/bin/python3.12

from pyaoc import Env

e = Env(9)
e.T("{}", 1, None)
e.T("{{{}}}", 6, None)
e.T("{{},{}}", 5, None)
e.T("{{{},{},{{}}}}", 16, None)
e.T("{<a>,<a>,<a>,<a>}", 1, None)
e.T("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9, None)
e.T("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9, None)
e.T("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3, None)

e.T("{<>}", None, 0)
e.T("{<random characters>}", None, 17)
e.T("{<<<<>}", None, 3)
e.T("{<{!>}>}", None, 2)
e.T("{<!!>}", None, 0)
e.T("{<!!!>>}", None, 0)
e.T("{<{o\"i!a,<{i<a>}", None, 10)


def skip_garbage(soup, pos):
    escape = False
    removed = 0
    while True:
        assert pos < len(soup)
        c = soup[pos]
        pos += 1
        if escape:
            escape = False
            continue
        if c == '!':
            escape = True
        elif c == '>':
            break
        else:
            removed += 1
    return pos, removed


def sum_groups(soup, pos, current) -> tuple[int, int, int]:
    total = current
    garbage = 0
    while True:
        assert pos < len(soup), str(pos)
        c = soup[pos]
        pos += 1
        if c == '{':
            v, pos, g = sum_groups(soup, pos, current + 1)
            total += v
            garbage += g
        elif c == '}':
            break
        elif c == '<':
            pos, g = skip_garbage(soup, pos)
            garbage += g
    return total, pos, garbage


def part1(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    soup = lines[0]
    assert soup[0] == '{'
    val, _, _ = sum_groups(soup, 1, 1)
    return val


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    soup = lines[0]
    assert soup[0] == '{'
    _, _, garbage = sum_groups(soup, 1, 1)
    return garbage


e.run_tests(2, part2)
e.run_main(2, part2)
