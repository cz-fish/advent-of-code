#!/usr/bin/env python3

from pyaoc import Env
import re

e = Env(4)
e.T("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""", 240, 4455)


def parse_event(event):
    m = re.match(r'^\[1518-(\d\d)-(\d\d) (\d\d):(\d\d)\] (.*)', event)
    assert m is not None, f"Cannot parse line {event}"
    _d, _m, _h, _mm, what = m.groups()
    # day = int(_d)
    # month = int(_m)
    # hour = int(_h)
    minute = int(_mm)
    return minute, what


def process_events(input, wakeup_func, state):
    inp = sorted(input.get_valid_lines())

    current = None
    slept = None

    for ev in inp:
        minute, what = parse_event(ev)

        if what == 'wakes up':
            assert slept is not None, f'wakes up without sleeping: {ev}'
            assert current is not None, f'wakes up, no guard: {ev}'
            wakeup_func(state, current, slept, minute)
            slept = None

        elif what == 'falls asleep':
            assert current is not None, f'falls asleep, no guard: {ev}'
            assert slept is None, f'falls asleep, already asleep: {ev}'
            slept = minute

        elif what.startswith('Guard '):
            mm = re.search(r'Guard #(\d+) begins', what)
            assert mm is not None, f'cannot parse start of shift: {ev}'
            current = int(mm.groups()[0])


def wakeup_part1(state, current, slept, minute):
    if current not in state.guards:
        state.guards[current] = [0, [0]*60]
    g = state.guards[current]
    g[0] += minute - slept
    for i in range(slept, minute):
        g[1][i] += 1
    if g[0] > state.maxminute:
        state.maxminute = g[0]
        state.maxguard = current


class State:
    def __init__(self):
        self.guards = {}
        self.maxminute = 0
        self.maxguard = None


def part1(input):
    state = State()
    process_events(input, wakeup_part1, state)

    g = state.guards[state.maxguard]
    maxm = 0
    maxv = g[1][0]
    for i in range(1, 60):
        if g[1][i] > maxv:
            maxv = g[1][i]
            maxm = i

    print(f'Guard {state.maxguard}, minute {maxm}')
    return state.maxguard * maxm


e.run_tests(1, part1)
e.run_main(1, part1)


def wakeup_part2(state, current, slept, minute):
    if current not in state.guards:
        state.guards[current] = [[0, 0], [0]*60]
    g = state.guards[current]
    for i in range(slept, minute):
        g[1][i] += 1
        if g[1][i] > g[0][0]:
            g[0][0] = g[1][i]
            g[0][1] = i
    if g[0][0] > state.maxminute:
        state.maxminute = g[0][0]
        state.maxguard = current


def part2(input):
    state = State()
    process_events(input, wakeup_part2, state)
    g = state.guards[state.maxguard]
    maxm = g[0][1]
    print(f'Guard {state.maxguard}, minute {maxm}')
    return state.maxguard * maxm


e.run_tests(2, part2)
e.run_main(2, part2)
