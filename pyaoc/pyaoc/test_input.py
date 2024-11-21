from . import Input
import os.path

IFILE = os.path.join(os.path.dirname(__file__), "test_input.txt")


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


def test_get_all_ints():
    inp = Input(IFILE, ["""1 2 3 4 19 5
1e4
"""])
    inp.use_test(0)
    i = inp.get_all_ints()
    assert(len(i) == 8)
    assert(i == [1, 2, 3, 4, 19, 5, 1, 4])


def test_read_stripped_lines():
    inp = Input(IFILE, ["""1
                        2
                        3"""], raw_lines=False)
    inp.use_test(0)
    ln = inp.get_lines()
    assert(len(ln) == 3)
    assert(ln[0] == "1")
    assert(ln[1] == "2")
    assert(ln[2] == "3")


def test_read_raw_lines():
    # Note: reading from the provided test string is not really the same as reading from the
    # input file, as the test lines don't have \n at the end, but when read from a file, they
    # would have
    inp = Input(IFILE, ["""1
                        2
                        3"""], raw_lines=True)
    inp.use_test(0)
    ln = inp.get_lines()
    assert(len(ln) == 3)
    assert(ln[0] == "1")
    assert(ln[1] == "                        2")
    assert(ln[2] == "                        3")


def test_get_valid_lines():
    # Note: when using the test input, the Input class doesn't do trimming, so the get_valid_lines
    # only removes completely empty lines. For the real input, it would trim first and then remove
    # empty lines, thus also removing lines with only whitespace characters. But we would need to
    # test that against a real input file.
    inp = Input(IFILE, ["""123

.

x"""])
    inp.use_test(0)
    ln = inp.get_valid_lines()
    assert(len(ln) == 3)
    assert(ln[0] == "123")
    assert(ln[1] == ".")
    assert(ln[2] == "x")


def test_use_main_input():
    inp = Input(IFILE, ["""123
456"""])
    inp.use_test(0)
    ln = inp.get_all_ints()
    assert(len(ln) == 2)
    inp.use_main_input()
    ln = inp.get_all_ints()
    assert(len(ln) == 4)
