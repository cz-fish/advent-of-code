#!/usr/bin/env python3
import intcode
import threading
from itertools import permutations

with open('input23.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

queues = {}
inpos = {}
for i in range(50):
    queues[i] = [i]
    inpos[i] = 0
idle = set()
maybe_idle = set()
nat_queue = [0, 0]

last_nat_y = None
stop = False

mutex = threading.Lock()

def nat_trigger():
    global queues
    global idle
    global last_nat_y
    global inpos
    global stop

    global mutex
    with mutex:
        for i in range(50):
            if inpos[i] < len(queues[i]):
                return

        print('All idle, sending resume from NAT', nat_queue)
        idle.remove(0)
        if nat_queue[1] == last_nat_y:
            print('Y sent from NAT twice in row:', last_nat_y)
            stop = True
        queues[0] += nat_queue[:]
        last_nat_y = nat_queue[1]


def nic_thread(n):
    mach = intcode.IntCode(program)
    output = []

    def input_fn():
        global queues
        global idle
        global maybe_idle
        global inpos
        global stop
        if stop:
            # We need to stop; the result has been found. The easiest
            # (although very dirty) way is to just crash all the 50 threads.
            raise RuntimeError("Stop")
        # print(f'Mach {n} asking for input')
        if inpos[n] < len(queues[n]):
            val = queues[n][inpos[n]]
            inpos[n] += 1
            if n in idle:
                idle.remove(n)
            if n in maybe_idle:
                maybe_idle.remove(n)
        else:
            val = -1
            if n in idle:
                # already idle
                if len(idle) == 50:
                    nat_trigger()
            elif n in maybe_idle:
                # becoming idle
                idle.add(n)
                maybe_idle.remove(n)
                print(f'Idle {len(idle)}')
                if len(idle) == 50:
                    nat_trigger()
            else:
                # will become idle next time
                maybe_idle.add(n)
        return val

    def output_fn(v):
        global queues
        global nat_queue
        global idle
        global maybe_idle
        nonlocal output
        if n in idle:
            idle.remove(n)
        if n in maybe_idle:
            maybe_idle.remove(n)
        # print(f'Mach {n} producing output {v}')
        output += [v]
        if len(output) == 3:
            # complete packet
            dest = output[0]
            if dest == 255:
                nat_queue[0] = output[1]
                nat_queue[1] = output[2]
                print('Packet to NAT:', output[1], output[2])
            else:
                queues[dest] += output[1:]
                print(f'Mach {n} sends packet to {dest}: {output[1:]}')
            output = []

    mach.run(input_fn, output_fn)


threads = [
    threading.Thread(target=nic_thread, kwargs={'n': i})
    for i in range(50)
]
for t in threads:
    t.start()

for t in threads:
    t.join()

