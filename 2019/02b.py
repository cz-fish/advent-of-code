#!/usr/bin/env python3
import sys

with open('input02.txt', 'rt') as f:
    l = f.readline().strip()

reset_state = [int(i) for i in l.split(',')]


def run(noun, verb, mem):
    state[1] = noun
    state[2] = verb

    pos = 0
    while True:
        op = mem[pos]
        if op == 99:
            break
        a = mem[mem[pos+1]]
        b = mem[mem[pos+2]]
        d = mem[pos+3]
        if op == 1:
            r = a + b
        elif op == 2:
            r = a * b
        else:
            return False
        mem[d] = r
        pos += 4

    return True


for noun in range(100):
    for verb in range(100):
        state = reset_state[:]
        success = run(noun, verb, state)
        if not success:
            continue
        print(noun, verb, state[0], success)
        if state[0] == 19690720:
            print(noun * 100 + verb)
            sys.exit(0)

print('no result')
