#!/usr/bin/python3.8

from aoc import Env

e = Env(8)
e.T("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf", 0, 5353)
e.T("""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""", 26, 61229)

def split_input(line):
    vals = line.strip().split(' ')
    assert len(vals) == 15
    return vals[:10], vals[-4:]


def part1(input):
    counter = 0
    for line in input.get_valid_lines():
        _, right = split_input(line)
        counter += sum([1 for x in right if len(x) in [2,3,4,7]])
    return counter


e.run_tests(1, part1)
e.run_main(1, part1)


"""
  0
1   2
  3
4   5
  6
"""
digits = {
    0: set([0, 1, 2, 4, 5, 6]), # missing 3
    1: set([2, 5]),
    2: set([0, 2, 3, 4, 6]),    # missing 1, 5
    3: set([0, 2, 3, 5, 6]),    # missing 1, 4
    4: set([1, 2, 3, 5]),
    5: set([0, 1, 3, 5, 6]),    # missing 2, 4
    6: set([0, 1, 3, 4, 5, 6]), # missing 2
    7: set([0, 2, 5]),
    8: set([0, 1, 2, 3, 4, 5, 6]),
    9: set([0, 1, 2, 3, 5, 6])  # missing 4
}


def make_map(left):
    left.sort(key=lambda k: len(k))
    sets = [set(x) for x in left]

    all = set([chr(i + ord('a')) for i in range(7)])
    one = sets[0]
    seven = sets[1]
    four = sets[2]
    # missing from the 6-long are segments 2, 3, 4
    seg234 = (all - sets[8]).union(all - sets[7]).union(all - sets[6])
    assert len(seg234) == 3
    # missing from the 5-long are segments 1, 2, 4, 5
    seg1245 = (all - sets[5]).union(all - sets[4]).union(all - sets[3])
    assert len(seg1245) == 4

    # what is in seven and not in one is segment 0
    seg0 = seven - one
    assert len(seg0) == 1

    # what is in four and not in one is 1, 3
    seg13 = four - one

    seg3 = seg13.intersection(seg234)
    assert len(seg3) == 1

    seg1 = seg13 - seg3
    assert len(seg1) == 1

    seg24 = seg234 - seg3
    assert len(seg24) == 2
    seg5 = seg1245 - seg24 - seg1
    assert len(seg5) == 1

    seg6 = all - seg1245 - seg0 - seg3
    assert len(seg6) == 1

    # one of the 5-longs is missing 1 and 4 (and not missing 5). We know
    # what 1 and 5 are, so we can deduce 4
    for i in [3, 4, 5]:
        fivelong = sets[i]
        if fivelong.intersection(seg5) and not fivelong.intersection(seg1):
            seg4 = all - fivelong - seg1
            assert len(seg4) == 1
            break
    else:
        assert False
    
    seg2 = seg24 - seg4
    assert len(seg2) == 1

    return {
        0: list(seg0)[0],
        1: list(seg1)[0],
        2: list(seg2)[0],
        3: list(seg3)[0],
        4: list(seg4)[0],
        5: list(seg5)[0],
        6: list(seg6)[0],
    }


def decode_right(right, seg_map):
    val = 0
    for digit in right:
        segs = set([seg_map[c] for c in digit])
        digit_val = [d for d, s in digits.items() if s == segs]
        assert len(digit_val) == 1
        val = val * 10 + digit_val[0]
    return val


def part2(input):
    total = 0
    for line in input.get_valid_lines():
        left, right = split_input(line)
        seg_map = make_map(left)
        rev_seg_map = {k: v for v, k in seg_map.items()}
        val = decode_right(right, rev_seg_map)
        total += val
    return total


e.run_tests(2, part2)
e.run_main(2, part2)

