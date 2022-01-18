#!/usr/bin/python3.8

from aoc import Env

e = Env(12)
#e = Env(13, different_input='input12-old.txt')

e.T("""initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""", 325, None)

# Input I've got before, and validated with the solution in the 2018-old/ directory
# Can now be used as a test case for part 2
e.T("""initial state: ###.......##....#.#.#..###.##..##.....#....#.#.....##.###...###.#...###.###.#.###...#.####.##.#....#

..... => .
#..## => .
..### => #
..#.# => #
.#.#. => .
####. => .
##.## => #
#.... => .
#...# => .
...## => .
##..# => .
.###. => #
##### => #
#.#.. => #
.##.. => #
.#.## => .
...#. => #
#.##. => #
..#.. => #
##... => #
....# => .
###.# => #
#..#. => #
#.### => #
##.#. => .
###.. => #
.#### => .
.#... => #
..##. => .
.##.# => .
#.#.# => #
.#..# => .""", None, 2600000001872)


class Line:
    def __init__(self, pattern=""):
        self.left = []
        self.right = [c for c in pattern]
        
    def min(self):
        for i in range(len(self.left) - 1, -1, -1):
            if self.left[i] == '#':
                return -i - 1
        return 0

    def max(self):
        for i in range(len(self.right) - 1, -1, -1):
            if self.right[i] == '#':
                return i
        return 0

    def get(self, pos):
        if pos >= 0:
            if pos >= len(self.right):
                return '.'
            else:
                return self.right[pos]
        else:
            if -pos >= len(self.left):
                return '.'
            else:
                return self.left[-pos - 1]

    def put(self, pos, char):
        if pos >= 0:
            if pos >= len(self.right):
                self.right += ['.'] * (pos - len(self.right) + 1)
            self.right[pos] = char
        else:
            pos = -pos - 1
            if pos >= len(self.left):
                self.left += ['.'] * (pos - len(self.left) + 1)
            self.left[pos] = char

    def get_plants(self):
        plants = [
            -i - 1 for i, x in enumerate(self.left) if x == '#'
        ] + [
            i for i, x in enumerate(self.right) if x == '#'
        ]
        return plants

    def __repr__(self):
        s = f"{self.min()}..{self.max()}: "
        for x in range(self.min(), self.max() + 1):
            s += self.get(x)
        return s


def load_input(input):
    gr = input.get_groups()
    assert len(gr) == 2
    assert len(gr[0]) == 1
    assert gr[0][0].startswith('initial state: ')
    state = gr[0][0][len('initial state: '):].strip()
    rules = {}
    for ln in gr[1]:
        ln = ln.strip()
        a, b = ln.split(' => ')
        rules[a] = b
    return state, rules


def grow(state, rules, generations):
    line = Line(state)
    # print('0 ' + str(line))
    for i in range(generations):
        newLine = Line()
        for j in range(line.min() - 2, line.max() + 2 + 1):
            pattern = ''
            for k in range(-2, 3):
                pattern += line.get(j + k)
            if pattern not in rules:
                newLine.put(j, '.')
            else:
                newLine.put(j, rules[pattern])
        line = newLine
        #if i >= 150 and i <= 160:
        #    print(f"{i+1} {line}")
    return line


def part1(input):
    state, rules = load_input(input)
    final_state = grow(state, rules, 20)
    return sum(final_state.get_plants())


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    state, rules = load_input(input)

    """
    Given the rules in my input, after about 100 iterations, the pattern stabilizes:
    ###.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#
    and then it only floats to the right by 1 position in every generation

    So we take a high enough iteration and find the position of the first plant. We move the pots to the right by
    as many positions as remain till 50000000000, and then we have our final configuration
    """

    state200 = grow(state, rules, 200)
    offset = 50000000000 - 200
    total = 0
    for i in range(state200.min(), state200.max() + 1):
        if state200.get(i) == '#':
            total += offset + i
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
