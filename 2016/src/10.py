#!/usr/bin/python3.8

import re
from collections import deque


init_re = re.compile(r'^value (\d+) goes to bot (\d+)$')
give_re = re.compile(r'^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$')

gives = deque()
bots = {}

with open('../input10.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        if not ln:
            continue
        m = init_re.match(ln)
        if m is not None:
            gives.append((int(m.group(1)), int(m.group(2))))
        else:
            m = give_re.match(ln)
            assert m is not None, f"Parsing line failed: '{ln}'"
            bot = int(m.group(1))
            low_target = (m.group(2), int(m.group(3)))
            high_target = (m.group(4), int(m.group(5)))
            assert bot not in bots, f"Duplicate definition for bot {bot}"
            bots[bot] = (low_target, high_target, [])

outputs = {}


def give(target, val):
    global outputs
    global gives
    who, which = target
    if who == 'bot':
        gives.append((val, which))
    elif who == 'output':
        assert which not in outputs, f"Multiple values pushed to the same output {which}"
        outputs[which] = val
    else:
        assert False, f"Wrong give target '{who}'"


while gives:
    val, to = gives.popleft()
    assert to in bots, f"Attempting to give value {val} to bot {bot} which doesn't exist"
    low_target, high_target, vals = bots[to]
    if vals:
        assert len(vals) == 1, f"Bot {to} has unexpected number of values (expected 1 value): {vals}"
        # Give both values
        high = max(val, vals[0])
        low = min(val, vals[0])

        if high == 61 and low == 17:
            print(f"Part 1: bot {to}")

        give(low_target, low)
        give(high_target, high)
    else:
        # This is the first value
        vals.append(val)

assert 0 in outputs and 1 in outputs and 2 in outputs, f"One of the expected outputs was not produced"
print(f"Part 2: {outputs[0] * outputs[1] * outputs[2]}")
