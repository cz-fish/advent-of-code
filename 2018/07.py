#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict
import re
import heapq

e = Env(7, [], {'workers': 5, 'timeadd': 60})
e.T("""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""",
    "CABDFE",
    15, {'workers': 2, 'timeadd': 0})


def make_graph(lines):
    r = re.compile(r'Step (.) must.*step (.) can')
    req = defaultdict(str)
    prov = defaultdict(str)
    possible = set()
    used = set()
    for ln in lines:
        m = r.match(ln)
        assert m is not None
        f = m.group(1)
        t = m.group(2)
        prov[f] += t
        req[t] += f
        possible.add(f)
        used.add(t)
    return req, prov, possible - used


def unblock(what, unblocked, req, prov):
    for c in prov[what]:
        p = req[c].replace(what, '')
        if not p:
            # c is now unblocked
            heapq.heappush(unblocked, c)
            del req[c]
        else:
            req[c] = p


def part1(input):
    req, prov, start = make_graph(input.get_valid_lines())
    unblocked = list(start)
    heapq.heapify(unblocked)

    result = ''
    while unblocked:
        n = heapq.heappop(unblocked)
        result += n
        unblock(n, unblocked, req, prov)

    return result


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    req, prov, start = make_graph(input.get_valid_lines())
    unblocked = list(start)
    heapq.heapify(unblocked)
    workers = e.get_param()['workers']
    timeadd = e.get_param()['timeadd']
    busy = [None] * workers
    idle = set([i for i in range(workers)])
    timer = 0
    order = ''
    while unblocked or (len(idle) < workers):
        # finish tasks
        for w in range(workers):
            if busy[w] and busy[w][0] == timer:
                # worker w has just finished task
                _, item = busy[w]
                order += item
                busy[w] = None
                idle.add(w)
                unblock(item, unblocked, req, prov)
        # schedule tasks
        for w in range(workers):
            if not busy[w] and unblocked:
                work = heapq.heappop(unblocked)
                endtime = timer + timeadd + ord(work) - ord('A') + 1
                busy[w] = (endtime, work)
                idle.remove(w)

        timer += 1
    print(f"Finished in order {order}")
    return timer - 1


e.run_tests(2, part2)
e.run_main(2, part2)
