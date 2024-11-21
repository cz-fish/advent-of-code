#!/usr/bin/python3.8

from pyaoc import Env, Integers

e = Env(8)
e.T("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""", 2, None)

e.T("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""", 6, None)

e.T("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""", None, 6)

def parse_links(node_desc):
    nodes = {}
    for ln in node_desc:
        assert len(ln) == 16
        assert ln[4] == '='
        assert ln[15] == ')'
        source = ln[:3]
        left = ln[7:10]
        right = ln[12:15]
        nodes[source] = (left, right)
    return nodes

def reach_node(start, end, instr, nodes):
    where = start
    steps = 0
    while where != end:
        i = instr[steps % len(instr)]
        where = nodes[where][0 if i == 'L' else 1]
        steps += 1
    return steps

def part1(input):
    instr_desc, node_desc = input.get_groups()
    instr = instr_desc[0]
    nodes = parse_links(node_desc)
    return reach_node('AAA', 'ZZZ', instr, nodes)


e.run_tests(1, part1)
e.run_main(1, part1)


def reach_any_z_node(start, instr, nodes):
    reached = {}
    where = start
    steps = 0
    while True:
        i = steps % len(instr)
        if where[-1] == 'Z':
            if where in reached:
                #print(f"reached {where} with i={i}")
                # we've reached the same Z node again, is it at the same instruction as well?
                if i in reached[where]:
                    # it was, so this is a period
                    # it's the shortest offset + period, but not necessarily the shortest period
                    # TODO: is that going to be a problem? Answer - not given the properties of the input
                    offset = reached[where][i]
                    period = steps - offset
                    return offset, period
                reached[where][i] = steps
            else:
                #print(f"reached {where} for the first time. i={i}")
                # new Z node reached
                reached[where] = {i : steps}
        where = nodes[where][0 if instr[i] == 'L' else 1]
        steps += 1


def part2(input):
    instr_desc, node_desc = input.get_groups()
    instr = instr_desc[0]
    nodes = parse_links(node_desc)
    all_paths = {}
    for node in nodes.keys():
        if node[-1] != 'A':
            continue
        all_paths[node] = reach_any_z_node(node, instr, nodes)
    #print(all_paths)
    # Find lowest common multiple of all the periods + also account for different offsets
    # Note: given the input, all offsets can be ignored, because all paths are just simple loops
    lcm = 1
    for _, period in all_paths.values():
        lcm = Integers.lcm(lcm, period)
    return lcm


e.run_tests(2, part2)
e.run_main(2, part2)
