#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict, deque
import heapq

e = Env(25, param="25.dot")
e.T("""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""", 54, None, param="25t.dot")


def parse_input(input):
    dot = "graph {\n"
    graph = defaultdict(set)
    for ln in input.get_valid_lines():
        left, right = ln.split(": ")
        dst = right.split()
        for node in dst:
            graph[left].add(node)
            graph[node].add(left)
            dot += f"    {left} -- {node}\n"
    dot += "}"
    return graph, dot


def find_cuts(graph):
    counters = defaultdict(int)
    for start in graph.keys():
        q = deque([start])
        prev_nodes = {start: None}
        while q:
            pos = q.popleft()
            for nei in graph[pos]:
                if nei not in prev_nodes:
                    prev_nodes[nei] = pos
                    q.append(nei)
        for node0, node1 in prev_nodes.items():
            if node1 is None:
                continue
            edge = (min(node0, node1), max(node0, node1))
            counters[edge] += 1
    sorted_edges = []
    for edge, usage in counters.items():
        heapq.heappush(sorted_edges, (-usage, edge))
    assert len(sorted_edges) >= 3
    return [heapq.heappop(sorted_edges)[1] for _ in range(3)]


def count_nodes(graph, start):
    visited = set([start])
    q = deque([start])
    while q:
        node = q.popleft()
        for n in graph[node]:
            if n not in visited:
                q.append(n)
                visited.add(n)
    return len(visited)


def part1(input):
    fname = e.get_param()
    graph, dot = parse_input(input)
    #with open(fname, "wt") as f:
    #    print(dot, file=f)

    ## 3 cuts found by rendering the graph with the neato engine of graphviz
    #cuts = [('tqr', 'grd'), ('tqh', 'dlv'), ('ngp', 'bmd')]
    cuts = find_cuts(graph)

    for first, second in cuts:
        assert second in graph[first], print(f"{first}, {second}")
        graph[first].remove(second)
        graph[second].remove(first)
    return count_nodes(graph, cuts[0][0]) * count_nodes(graph, cuts[0][1])


e.run_tests(1, part1)
e.run_main(1, part1)


