from aoc import Input

IFILE = '../input01.txt'


def test_read_file():
    inp = Input(IFILE)
    ints = inp.get_ints()
    assert(len(ints) == 200)
    assert(ints[0] == 1918)
    assert(ints[-1] == 1407)


def test_use_tests():
    inp = Input(IFILE, ["""abc
def
""", """ghi"""])
    inp.use_test(0)
    ls = inp.get_lines()
    assert(len(ls) == 3)
    assert(ls == ["abc", "def", ""])
    inp.use_test(1)
    ls = inp.get_lines()
    assert(len(ls) == 1)
    assert(ls == ["ghi"])


def test_get_groups():
    inp = Input(IFILE, ["""abc def
ghi jkl

xyz
abc
def
"""])
    inp.use_test(0)
    gr = inp.get_groups()
    assert(len(gr) == 2)
    assert(len(gr[0]) == 2)
    assert(gr[0] == ['abc def', 'ghi jkl'])
    assert(len(gr[1]) == 3)
    assert(gr[1] == ['xyz', 'abc', 'def'])


def test_get_ints():
    inp = Input(IFILE, ["""123
456
7
0
"""])
    inp.use_test(0)
    i = inp.get_ints()
    assert(len(i) == 4)
    assert(i == [123, 456, 7, 0])


def test_get_ints_tolerant():
    inp = Input(IFILE, ["""123
456abc
gg7
foo
3
"""])
    inp.use_test(0)
    i = inp.get_ints_tolerant(-1)
    assert(len(i) == 5)
    assert(i == [123, 456, 7, -1, 3])

# TODO: use_main_input, get_valid_lines
