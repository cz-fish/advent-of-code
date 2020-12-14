from aoc.input import Input
from typing import Callable, List, NamedTuple, Optional, Type

RED = "\033[0;31m"
GREEN = "\033[0;32m"
CLR = "\033[0m"

# The result of each AOC puzzle is assume to be int
ResultType: Type[int] = int
OptResultType = Optional[ResultType]


# Specification of custom test case
#   - input as a (multiline) string and expected result for part 1 and part 2
class TestSpec(NamedTuple):
    input: str
    res1: OptResultType
    res2: OptResultType


class Env:
    """Environment for constructing input, test cases, and executing both
       test cases and the real problem input"""

    def __init__(self, day: int, tests: List[TestSpec] = []):
        self._day = day
        self._tests = tests
        self._inp = None

    def _ensure_input(self) -> Input:
        """If not already constructed, construct an aoc.Input from the
           current day number and test cases specified so far.
           Test cases defined later will be ignored."""
        if self._inp is None:
            self._inp = Input(f"input{self._day:02}.txt", [t.input for t in self._tests])
        return self._inp

    def T(self, input: str, result_p1: OptResultType, result_p2: OptResultType) -> None:
        """Define a test case"""
        assert self._inp is None, "Cannot define more test cases once input is constructed"
        self._tests += [TestSpec(input=input, res1=result_p1, res2=result_p2)]

    def test_spec(self, test: TestSpec) -> None:
        """Define a test case (as a TestSpec tuple)"""
        assert self._inp is None, "Cannot define more test cases once input is constructed"
        self._tests += [TestSpec(input=test.input, res1=test.res1, res2=test.res2)]

    def run_tests(self, part: int, code: Callable[[Input], ResultType]) -> None:
        """Run given code on all tests that have defined expected result for the given
           problem part (i.e. part 1 or part 2) and check their result."""
        input = self._ensure_input()
        for i, test in enumerate(self._tests):
            if part == 1:
                expect = test.res1
            elif part == 2:
                expect = test.res2
            else:
                assert False, f"Part has to be either 1 or 2, not {part}"

            if expect is None:
                continue

            input.use_test(i)
            try:
                result = code(input)
                if result != expect:
                    print(f"{RED}Test {i} FAILED: expected {expect}, got {result}{CLR}")
                else:
                    print(f"{GREEN}Test {i} SUCCEEDED: result {result}{CLR}")
            except:
                print(f"{RED}Exception in test {i} (expected result {expect}){CLR}")
                raise

    def run_main(self, part: int, code: Callable[[Input], ResultType]) -> None:
        """Run given code on the main problem input"""
        input = self._ensure_input()
        input.use_main_input()
        result = code(input)
        print(f"Day {self._day} Part {part}: {result}")
