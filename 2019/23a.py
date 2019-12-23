#!/usr/bin/env python3
import intcode
import threading
from itertools import permutations

with open('input23.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

queues = {}
for i in range(50):
    queues[i] = [i]

def nic_thread(n):
    mach = intcode.IntCode(program)
    inpos = 0
    output = []

    def input_fn():
        global queues
        nonlocal inpos
        # print(f'Mach {n} asking for input')
        if inpos < len(queues[n]):
            val = queues[n][inpos]
            inpos += 1
        else:
            val = -1
        return val

    def output_fn(v):
        global queues
        nonlocal output
        # print(f'Mach {n} producing output {v}')
        output += [v]
        if len(output) == 3:
            # complete packet
            dest = output[0]
            if dest == 255:
                print('Packet to 255:', output[1], output[2])
                import sys
                sys.exit(0)
            if dest not in queues:
                queues[dest] = []
            queues[dest] += output[1:]
            print(f'Mach {n} sends packet to {dest}: {output[1:]}')
            output = []

    mach.run(input_fn, output_fn)
    results[n] = mach.output[-1]
    # print(f'Final output of mach {n}: {results[n]}')

threads = [
    threading.Thread(target=nic_thread, kwargs={'n': i})
    for i in range(50)
]
for t in threads:
    t.start()

for t in threads:
    t.join()

print(queues[255])
