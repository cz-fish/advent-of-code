import re
from typing import List


class Input:
    def __init__(self, fname: str, tests: List[str] = []):
        """Initialize input with the name of the input file and
           optionally also a list of other test inputs (strings)"""
        self.tests = [
            test.split('\n')
            for test in tests
        ]
        self.test_num = None
        self._read_file(fname)

    def use_test(self, test_num: int):
        """Use test data (one of the tests passed to the constructor)
           instead of the default input from the file"""
        assert(test_num < len(self.tests))
        self.lines = self.tests[test_num]

    def get_lines(self) -> List[str]:
        """Get input as a list of trimmed strings"""
        return self.lines[:]

    def get_valid_lines(self) -> List[str]:
        """Get input as a list of trimmed strings, removing empty lines"""
        return [ln for ln in self.lines if ln]

    def get_groups(self) -> List[List[str]]:
        """Get input as a list of groups. Input is assumed to be
           separated by blank lines. Each group is a list of strings"""
        groups = [[]]
        for ln in self.lines:
            if not ln:
                groups += [[]]
            else:
                groups[-1] += [ln]
        if not groups[-1]:
            groups = groups[:-1]
        return groups

    def get_ints(self) -> List[int]:
        """Get input as a list of ints"""
        return [int(ln) for ln in self.lines if ln]

    def get_ints_tolerant(self, default:any = 0) -> List[int]:
        """Get input as a list of ints. Try to find ints even
           if the lines don't consist only of ints.
           Put `default` value in the list where we didn't
           find any number on the line"""
        ints = []
        r = re.compile(r'\d+')
        for ln in self.lines:
            if not ln:
                continue
            m = r.search(ln)
            if m is not None:
                ints += [int(m.group(0))]
            else:
                ints += [default]
        return ints

    def _read_file(self, fname: str) -> None:
        with open(fname, 'rt') as f:
            self.lines = [ln.strip() for ln in f.readlines()]
