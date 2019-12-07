#!/usr/bin/env python3
import intcode
import threading
from itertools import permutations

with open('input07.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]


def run_with_settings(p):
    inputs = [[p[i]] for i in range(5)]
    inputs[0] += [0]
    results = [0] * 5
    conds = [threading.Condition() for i in range(5)]

    def amp_thread(n, a):
        nonlocal inputs
        nonlocal results
        mach = intcode.IntCode(program)
        inpos = 0
        next = (n + 1) % 5

        def input_fn():
            nonlocal inpos
            nonlocal conds
            # print(f'Mach {n} asking for input')
            with conds[n]:
                if inpos >= len(inputs[n]):
                    conds[n].wait()
            val = inputs[n][inpos]
            inpos += 1
            # print(f'Mach {n} getting input {val}')
            return val

        def output_fn(v):
            nonlocal inputs
            # print(f'Mach {n} producing output {v}')
            with conds[next]:
                inputs[next] += [v]
                conds[next].notify()

        mach.run(input_fn, output_fn)
        results[n] = mach.output[-1]
        # print(f'Final output of mach {n}: {results[n]}')

    threads = [
        threading.Thread(target=amp_thread, args=(i, p[i]))
        for i in range(5)
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return results[4]


amps = list(range(5, 10))
best = 0

for p in permutations(amps):
    val = run_with_settings(p)
    print(p, val)
    if val > best:
        best = val
    prev = 0

print(best)
