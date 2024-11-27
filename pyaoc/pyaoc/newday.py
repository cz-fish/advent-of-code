#!/usr/bin/python3.12

from datetime import datetime
import os
import sys

_template = r"""#!/usr/bin/python3.12

from pyaoc import Env

e = Env({{day}})


def part1(input):
    pass


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
"""


def generate_new_day():
    if len(sys.argv) > 1:
        day = int(sys.argv[1])
    else:
        day = datetime.now().day

    print(f"Day {day:02}")

    template = _template.replace("{{day}}", str(day))

    fname = f"{day:02}.py"

    with open(fname, "wt") as tgtf:
        tgtf.write(template)

    os.chmod(fname, 0o755)
