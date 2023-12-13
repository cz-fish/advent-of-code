#!/usr/bin/python3.8

from aoc import Env

e = Env(13)
e.T("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""", 405, 400)


def all_matches(lines, mirror_point):
    first = mirror_point - 1
    second = mirror_point
    assert first >= 0
    while first >= 0 and second < len(lines):
        if lines[first] != lines[second]:
            return False
        first -= 1
        second += 1
    return True


def find_mirror(lines):
    prev = None
    for i, ln in enumerate(lines):
        if prev is not None and ln == prev and all_matches(lines, i):
            return i
        prev = ln
    return 0


def transpose_pattern(pattern):
    return [
        ''.join([pattern[j][i] for j in range(len(pattern))]) for i in range(len(pattern[0]))
    ]


def part1(input):
    patterns = input.get_groups()
    left = 0
    above = 0
    for pattern in patterns:
        left += find_mirror(transpose_pattern(pattern))
        above += find_mirror(pattern)
    return left + 100 * above


e.run_tests(1, part1)
e.run_main(1, part1)


def test_symmetry_with_smudge(pattern, offset):
    def diffs(line1, line2):
        return sum([1 for i in range(len(line1)) if line1[i] != line2[i]])

    first = offset - 1
    second = offset
    smudges = 0
    while first >= 0 and second < len(pattern):
        if pattern[first] != pattern[second]:
            smudges += diffs(pattern[first], pattern[second])
            if smudges > 1:
                return False
        first -= 1
        second += 1
    return smudges == 1


def find_mirror_smudged(pattern):
    trans = transpose_pattern(pattern)
    nonsmudged_l = find_mirror(trans)
    nonsmudged_a = find_mirror(pattern)
    for left in range(1, len(trans)):
        if left != nonsmudged_l and test_symmetry_with_smudge(trans, left):
            break
    else:
        left = 0

    for above in range(1, len(pattern)):
        if above != nonsmudged_a and test_symmetry_with_smudge(pattern, above):
            break
    else:
        above = 0

    assert left != 0 or above != 0
    assert left == 0 or above == 0
    return left, above


def part2(input):
    patterns = input.get_groups()
    left = 0
    above = 0
    for pattern in patterns:
        l, a  = find_mirror_smudged(pattern)
        left += l
        above += a
    return left + 100 * above


e.run_tests(2, part2)
e.run_main(2, part2)
