#!/usr/bin/python3.8

# Note: https://oeis.org/A181391

# Stripped down and hardcoded for pypy.
#   c:\apps\pypy3.7-v7.3.3-win32\pypy3.exe 15-for-pypy.py
#   > 2424 0.7239582
# (first run - compilation - takes quite a bit of time, but
#  repeated runs are under 1 second)

from timeit import default_timer as timer


def van_eck(start, K):
    memory = [0] * K

    for i, x in enumerate(start):
        memory[x] = i + 1

    last_said = 0
    # Assuming all numbers in start are unique
    next = 0
    turn = len(start) + 1

    while turn <= K:
        # elf says next
        last_said = next
        # when was that said last time
        next = memory[last_said]
        if next != 0:
            next = turn - next
        memory[last_said] = turn
        turn += 1
    return last_said


start = timer()
res = van_eck([13,16,0,12,15,1], 30000000)
end = timer()
print(res, end-start)
