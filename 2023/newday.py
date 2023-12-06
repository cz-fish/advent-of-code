#!/usr/bin/python3.8

from datetime import datetime
import os
import sys

if len(sys.argv) > 1:
    day = int(sys.argv[1])
else:
    day = datetime.now().day

print(f"Day {day:02}")

with open("template.txt", "rt") as sourcef:
    template = sourcef.read()

template = template.replace("{{day}}", str(day))

fname = f"{day:02}.py"

with open(fname, "wt") as tgtf:
    tgtf.write(template)

os.chmod(fname, 0o755)
