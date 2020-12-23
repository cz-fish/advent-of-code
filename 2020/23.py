#!/usr/bin/python3.8

from aoc import Env

e = Env(23)
e.T("389125467", 67384529, 149245887792)


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def make_nodes(start, add_to_million):
    for v in start:
        yield Node(v)
    if add_to_million:
        for i in range(max(start) + 1, 1_000_001):
            yield Node(i)


def make_move(current, nodemap):
    maxnum = len(nodemap)
    current_node = nodemap[current]
    taken = [current_node.next, current_node.next.next, current_node.next.next.next]
    taken_vals = [x.val for x in taken]
    current_node.next = current_node.next.next.next.next
    current_node.next.prev = current_node

    where = (current - 2) % maxnum + 1
    while where in taken_vals:
        where = (where - 2) % maxnum + 1

    after_node = nodemap[where]
    before_node = after_node.next
    after_node.next = taken[0]
    taken[0].prev = after_node
    before_node.prev = taken[-1]
    taken[-1].next = before_node


def make_circle(input, add_to_million):
    start = [int(c) for c in input.get_valid_lines()[0]]
    nodemap = {}
    # Make circle of cups
    first = None
    prev = None
    for node in make_nodes(start, add_to_million):
        nodemap[node.val] = node
        if first is None:
            first = node
        else:
            prev.next = node
            node.prev = prev
        prev = node
    prev.next = first
    first.prev = prev
    return start[0], nodemap


def part1(input):
    current, nodemap = make_circle(input, add_to_million=False)
    for _ in range(100):
        make_move(current, nodemap)
        current = nodemap[current].next.val

    current = nodemap[1].next
    result = 0
    while current.val != 1:
        result = result * 10 + current.val
        current = current.next
    return result


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    current, nodemap = make_circle(input, add_to_million=True)

    for _ in range(10_000_000):
        make_move(current, nodemap)
        current = nodemap[current].next.val

    node1 = nodemap[1]
    result = node1.next.val * node1.next.next.val
    return result


e.run_tests(2, part2)
e.run_main(2, part2)
