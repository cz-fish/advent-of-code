#!/usr/bin/python3.8

from datetime import datetime

day = datetime.now().day
with open("template.txt", "rt") as sourcef:
    template = sourcef.read()

template = template.replace("{{day}}", str(day))

with open(f"{day}.py", "wt") as tgtf:
    tgtf.write(template)
