#!/usr/bin/python3.12

from pyaoc import Env

e = Env(21)
e.T("""029A
980A
179A
456A
379A""", 126384, None)


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""


def apply_robot(instr, is_numpad):
    x = 2
    y = 3 if is_numpad else 0
    output = ""
    numpad = {
        (0, 0): '7',
        (1, 0): '8',
        (2, 0): '9',
        (0, 1): '4',
        (1, 1): '5',
        (2, 1): '6',
        (0, 2): '1',
        (1, 2): '2',
        (2, 2): '3',
        (1, 3): '0',
        (2, 3): 'A',
    }
    arrows = {
        (1, 0): '^',
        (2, 0): 'A',
        (0, 1): '<',
        (1, 1): 'v',
        (2, 1): '>',
    }
    for i in instr:
        if i == '<':
            x -= 1
        elif i == '^':
            y -= 1
        elif i == '>':
            x += 1
        elif i == 'v':
            y += 1
        elif i == 'A':
            d = numpad if is_numpad else arrows
            assert (x, y) in d
            output += d[(x, y)]
        else:
            assert False, f"wrong instruction {i}"
    return output


g_cache = {}
g_top_cache = {}


def numeric_code(code, intermediate_robots):
    coords = {
        '7': (0, 0),
        '8': (1, 0),
        '9': (2, 0),
        '4': (0, 1),
        '5': (1, 1),
        '6': (2, 1),
        '1': (0, 2),
        '2': (1, 2),
        '3': (2, 2),
        '0': (1, 3),
        'A': (2, 3),
    }
    x, y = coords['A']
    out = 0
    for key in code:
        tx, ty = coords[key]
        dx = tx - x
        dy = ty - y
        out += one_move(intermediate_robots, x, y, dx, dy, (0, 3))
        x = tx
        y = ty
    return out


def one_move(level, sx, sy, dx, dy, avoid):
    cache_key = (level, dx, dy, sx, sy)
    options = []
    def move_x(d):
        if d < 0: # left
            return '<' * abs(d)
        else: # right
            return '>' * d

    def move_y(d):
        if d < 0: # up
            return '^' * abs(d)
        else: # down
            return 'v' * d

    if dy == 0:
        options.append(move_x(dx) + 'A')
        # sx, sy coordinates don't matter for cache
        cache_key = (level, dx, dy, 0, 0)
    elif dx == 0:
        options.append(move_y(dy) + 'A')
        # sx, sy coordinates don't matter for cache
        cache_key = (level, dx, dy, 0, 0)
    else:
        # either upply dx first and then dy, or vice versa
        tx = sx + dx
        if (tx, sy) != avoid:
            # apply x first, then y
            options.append(move_x(dx) + move_y(dy) + 'A')
        ty = sy + dy
        if (sx, ty) != avoid:
            # apply first y then x
            options.append(move_y(dy) + move_x(dx) + 'A')
        if len(options) == 2:
            # sx, sy coordinates don't matter for cache
            cache_key = (level, dx, dy, 0, 0)
    assert options, f"There are no options to move from {sx},{sy} by {dx},{dy} and avoid {avoid}"

    cache = g_cache if avoid == (0, 0) else g_top_cache
    if cache_key in cache:
        return cache[cache_key]

    shortest = None
    if level == 0:
        options.sort(key=lambda x: len(x))
        shortest = len(options[0])
    else:
        for opt in options:
            expanded = next_robot_step(level - 1, opt)
            if shortest is None or expanded < shortest:
                shortest = expanded
    cache[cache_key] = shortest
    return shortest


def next_robot_step(level, instr):
    coords = {
        '^': (1, 0),
        'A': (2, 0),
        '<': (0, 1),
        'v': (1, 1),
        '>': (2, 1),
    }
    x, y = coords['A']
    out = 0
    for key in instr:
        tx, ty = coords[key]
        dx = tx - x
        dy = ty - y
        out += one_move(level, x, y, dx, dy, (0, 0))
        x = tx
        y = ty
    return out


def solve(input, intermediate_robots):
    global g_cache
    global g_top_cache
    g_cache = {}
    g_top_cache = {}
    total = 0
    for code in input.get_valid_lines():
        seq = numeric_code(code, intermediate_robots)
        v = seq * int(code[:-1])
        total += v
    return total


def part1(input):
    return solve(input, 2)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    return solve(input, 25)


e.run_tests(2, part2)
e.run_main(2, part2)
