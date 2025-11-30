#!/usr/bin/python3.12

from pyaoc import Env, Grid

e = Env(19, raw_lines=True)
e.T("""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """, "ABCDEF", 38)


def find_start(top_line):
    left = top_line.find('|')
    right = top_line.rfind('|')
    assert left == right
    assert left != -1
    return left


def trace_and_collect(g, col):
    def viable(ndir):
        nonlocal row, col, g
        nr = row + ndir[0]
        nc = col + ndir[1]
        if not g.is_in(nr, nc):
            return False
        if g.get(nr, nc) == ' ':
            return False
        return True
    row = 0
    d = (1, 0)
    collected = ""
    steps = 0
    while True:
        row += d[0]
        col += d[1]
        steps += 1
        if not g.is_in(row, col):
            break
        c = g.get(row, col)
        if c >= 'A' and c <= 'Z':
            collected += c
        elif c == '+':
            # change dir
            ndir1 = (d[1], d[0])
            ndir2 = (-d[1], -d[0])
            viable1 = viable(ndir1)
            viable2 = viable(ndir2)
            assert not (viable1 and viable2), f"both turns viable at {row}, {col}"
            assert (viable1 or viable2), f"no turn possible at {row}, {col}"
            if viable1:
                d = ndir1
            else:
                d = ndir2
        elif c == ' ':
            break
    return collected, steps

def part1(input):
    g = Grid(input.get_valid_lines())
    start = find_start(input.get_valid_lines()[0])
    return trace_and_collect(g, start)[0]


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    g = Grid(input.get_valid_lines())
    start = find_start(input.get_valid_lines()[0])
    return trace_and_collect(g, start)[1]


e.run_tests(2, part2)
e.run_main(2, part2)
