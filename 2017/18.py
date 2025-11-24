#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict, deque


e = Env(18)
e.T("""set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""", 4, None)
e.T("""snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""", None, 3)


def parse_input(input):
    program = []
    for l in input.get_valid_lines():
        parts = l.split(" ")
        assert len(parts) in [2,3]
        assert parts[0] in ["snd", "set", "add", "mul", "mod", "rcv", "jgz"]
        if parts[0] in ["snd", "rcv"]:
            assert len(parts) == 2
            parts.append(None)
        else:
            assert len(parts) == 3
        program.append(parts)
    return program


def value_of_first_rcv(program):
    def get_param(x):
        nonlocal regs
        if x >= 'a' and x <= 'z':
            return regs[x]
        else:
            return int(x)
    regs = defaultdict(int)
    last_sound = None
    pc = 0
    while True:
        if pc < 0 or pc >= len(program):
            assert False, "program terminated"
        instr, x, y = program[pc]
        if instr == "snd":
            last_sound = get_param(x)
        elif instr == "rcv":
            if get_param(x) != 0:
                return last_sound
        elif instr == "set":
            regs[x] = get_param(y)
        elif instr == "add":
            regs[x] = regs[x] + get_param(y)
        elif instr == "mul":
            regs[x] = regs[x] * get_param(y)
        elif instr == "mod":
            regs[x] = regs[x] % get_param(y)
        elif instr == "jgz":
            if get_param(x) > 0:
                pc += get_param(y) - 1
        pc += 1


def part1(input):
    program = parse_input(input)
    return value_of_first_rcv(program)


e.run_tests(1, part1)
e.run_main(1, part1)


def run(program, regs, other_que):
    def get_param(x):
        nonlocal regs
        if x >= 'a' and x <= 'z':
            return regs[x]
        else:
            return int(x)

    did_run = False
    sent_msgs = 0
    while True:
        if regs['pc'] < 0 or regs['pc'] >= len(program):
            break
        instr, x, y = program[regs['pc']]
        if instr == "snd":
            other_que.append(get_param(x))
            sent_msgs += 1
        elif instr == "rcv":
            q = regs['que']
            if not q:
                break
            regs[x] = q.popleft()
        elif instr == "set":
            regs[x] = get_param(y)
        elif instr == "add":
            regs[x] = regs[x] + get_param(y)
        elif instr == "mul":
            regs[x] = regs[x] * get_param(y)
        elif instr == "mod":
            regs[x] = regs[x] % get_param(y)
        elif instr == "jgz":
            if get_param(x) > 0:
                regs['pc'] += get_param(y) - 1
        regs['pc'] += 1
        did_run = True
    return did_run, sent_msgs


def part2(input):
    program = parse_input(input)
    regs = [defaultdict(int), defaultdict(int)]
    regs[0]['pc'] = 0
    regs[1]['pc'] = 0
    regs[0]['p'] = 0
    regs[1]['p'] = 1
    regs[0]['que'] = deque()
    regs[1]['que'] = deque()
    send_counter1 = 0
    while True:
        did_run1, _ = run(program, regs[0], regs[1]['que'])
        did_run2, sent = run(program, regs[1], regs[0]['que'])
        send_counter1 += sent
        if not (did_run1 or did_run2):
            break
    return send_counter1


e.run_tests(2, part2)
e.run_main(2, part2)
