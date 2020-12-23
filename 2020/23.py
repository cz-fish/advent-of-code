#!/usr/bin/python3.8

from aoc import Env

e = Env(23)
e.T("389125467", 67384529, 149245887792)

max_steps = 100
digits = 9
how_many = 3


def make_step(current_id, config):
    new_id = current_id
    current = config[current_id]

    # take next 3
    take = (config + config)[current_id + 1 : current_id + how_many + 1]
    if current_id >= digits - how_many:
        skip = how_many - (digits - current_id) + 1
        config = config[skip : current_id + 1]
        new_id -= skip
    else:
        config = config[:current_id+1] + config[current_id + how_many + 1:]
    # print(f'taken 3: {take}, rest: {config}, current_id {current_id}, new_id {new_id}')
    where = (current - 2) % digits + 1
    while where not in config:
        where = (where - 2) % digits + 1
    idx = config.index(where) + 1
    # print(f'looked for {where}, found it at {idx}')
    config = config[:idx] + take + config[idx:]
    if idx <= new_id:
        new_id += how_many
    # print(f'pasted: {config}, new_id: {new_id}')

    # shift config so that new_id is at the same position as current_id was
    while new_id != current_id:
        config = [config[-1]] + config[:-1]
        new_id = (new_id + 1) % digits

    return config


def part1(input):
    config = [int(c) for c in input.get_valid_lines()[0]]
    assert len(config) == digits
    for i in range(max_steps):
        config = make_step(i % digits, config)
    res_string = ''.join([str(x) for x in config])
    idx = res_string.index('1')
    res_string *= 2
    res = int(res_string[idx + 1: idx + digits])
    print(f"{max_steps}: {res_string} -> {res}")
    return res


e.run_tests(1, part1)
e.run_main(1, part1)


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def make_nodes(start):
    for v in start:
        yield Node(v)
    for i in range(max(start) + 1, 1_000_001):
        yield Node(i)


def make_move_pt2(current, nodemap):
    current_node = nodemap[current]
    taken = [current_node.next, current_node.next.next, current_node.next.next.next]
    taken_vals = [x.val for x in taken]
    current_node.next = current_node.next.next.next.next
    current_node.next.prev = current_node

    where = (current - 2) % 1_000_000 + 1
    while where in taken_vals:
        where = (where - 2) % 1_000_000 + 1

    after_node = nodemap[where]
    before_node = after_node.next
    after_node.next = taken[0]
    taken[0].prev = after_node
    before_node.prev = taken[-1]
    taken[-1].next = before_node


def part2(input):
    start = [int(c) for c in input.get_valid_lines()[0]]
    nodemap = {}
    # Make circle of cups
    first = None
    prev = None
    for node in make_nodes(start):
        nodemap[node.val] = node
        if first is None:
            first = node
        else:
            prev.next = node
            node.prev = prev
        prev = node
    prev.next = first
    first.prev = prev

    current = start[0]
    for _ in range(10_000_000):
        make_move_pt2(current, nodemap)
        current = nodemap[current].next.val

    node1 = nodemap[1]
    result = node1.next.val * node1.next.next.val
    return result


e.run_tests(2, part2)
e.run_main(2, part2)
