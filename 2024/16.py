#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Tuple
import heapq

def eT(*a): pass

e = Env(16)
e.T("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 7036, 45)

e.T("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""", 11048, 64)

e.T("""##############################
##.#.#.#.#.#########.#.#####.#
#..#...#.#.#E..#...#...#...#.#
########.#.###.#.#.###.#.#.#.#
##...#...#.#.#.#.#...#...#.#.#
##.#.#.###.###.#.###.#####.#.#
##.#...#...#.................#
##.#########.#########.#####.#
##...........#.......#.....#S#
##############################""", None, 23)

e.T("""###################
#########.#.#####.#
#E..#...#...#...#.#
###.#.#.###.#.#.#.#
#.#.#.#...#...#.#.#
###.#.###.#####.#.#
#.................#
#.#########.#####.#
#.#.......#.....#S#
###################""", None, 23)

e.T("""######
#S..##
#.#.##
#...E#
######""", 2005, 9)


def find_position(g, which_one):
    for row in range(g.h):
        for col in range(g.w):
            if g.get(row, col) == which_one:
                return row, col
    assert False, f"Position {which_one} not found"


def shortest_dfs(g, start, end):
    min_dists = {}
    q = deque()
    # E = 0, N = 1, W = 2, S = 3
    facing = 0
    steps = {
        0: (0, 1),
        1: (-1, 0),
        2: (0, -1),
        3: (1, 0)
    }
    q.append((start[0], start[1], facing, 0))
    while q:
        r, c, facing, score = q.pop()
        coords = (r, c, facing)
        if coords in min_dists and min_dists[coords] <= score:
            continue
        min_dists[coords] = score
        if coords == end:
            # no need to search any further from end
            continue
        # first turn around
        nscore = score + 1000
        q.append((r, c, (facing + 1) % 4, nscore))
        q.append((r, c, (facing - 1) % 4, nscore))
        # then continue in the same direction
        dr, dc = steps[facing]
        nr = r + dr
        nc = c + dc
        nfacing = facing
        nscore = score + 1
        if g.get(nr, nc) != '#':
            if (nr, nc, nfacing) not in min_dists or min_dists[(nr, nc, nfacing)] > nscore:
                q.append((nr, nc, nfacing, nscore))
    best = None
    for facing in range(4):
        coord = (end[0], end[1], facing)
        if coord not in min_dists:
            continue
        val = min_dists[coord]
        if best is None or val < best:
            best = val
    assert best is not None, f"Path to end {end} not found"
    return best


def find_nodes(g):
    """Node is either start position, or end position, or a
    free space with exits in at least 3 directions"""
    start = None
    end = None
    nodes = set()
    # Assuming there is a border around the maze, we can offset by 1
    for r in range(1, g.h - 1):
        for c in range(1, g.w - 1):
            what = g.get(r, c)
            if what == 'S':
                assert start is None, f"Multiple starts {start} {r},{c}"
                start = (r, c)
            elif what == 'E':
                assert end is None, f"Multiple ends {end} {r},{c}"
                end = (r, c)
            elif what == '.':
                exits = sum([1 for nr, nc in g.neighbors4(r, c) if g.get(nr, nc) != '#'])
                if exits >= 3:
                    nodes.add((r, c))
    assert start is not None, "Start not found"
    assert end is not None, "End not found"
    nodes.add(start)
    nodes.add(end)
    return start, end, nodes


@dataclass
class Edge:
    next_node: Tuple[int, int]
    score: int
    facing: int # direction when arrived to next_node
    steps: set # all positions along the way, including next node


k_facing = {
    0: (0, 1),
    1: (-1, 0),
    2: (0, -1),
    3: (1, 0)
}


def make_edge(g, r, c, facing, nodes):
    dr, dc = k_facing[facing]
    r += dr
    c += dc
    if g.get(r, c) == '#':
        return None
    visited = set([(r, c)])
    score = 1

    while True:
        if (r, c) in nodes:
            edge = Edge(next_node=(r, c), score=score, facing=facing, steps=visited)
            return edge
        dr, dc = k_facing[facing]
        if g.get(r + dr, c + dc) != '#':
            # step forward
            r += dr
            c += dc
            score += 1
            visited.add((r, c))
        else:
            # try left turn
            n_facing = (facing + 1) % 4
            dr, dc = k_facing[n_facing]
            if g.get(r + dr, c + dc) != '#':
                facing = n_facing
                score += 1000
                continue
            # try right turn
            n_facing = (facing - 1) % 4
            dr, dc = k_facing[n_facing]
            if g.get(r + dr, c + dc) != '#':
                facing = n_facing
                score += 1000
                continue
            # no turn possible; this must be a dead end
            return None


def make_smaller_graph(g, nodes):
    # For starting node -> for each direction -> an Edge
    connections = defaultdict(dict)
    for r, c in nodes:
        for facing in range(4):
            edge = make_edge(g, r, c, facing, nodes)
            if edge:
                connections[(r, c)][facing] = edge
    return connections


def get_turn_penalty(come_from, go_to):
    if come_from == go_to:
        # no turn
        return 0
    elif (go_to + 2) % 4 == come_from:
        # full turn
        return 2000
    else:
        # turn 90 degrees
        return 1000


def opposite_facing(f):
    return (f + 2) % 4


def reduce_dead_ends(graph, start, end):
    reduced = False
    nodes_to_remove = []
    nodes_to_reduce = []
    for node, edges in graph.items():
        if node == start or node == end:
            # do not reduce start or end
            continue
        if len(edges) == 1:
            # dead end - just remove
            nodes_to_remove.append(node)
        elif len(edges) == 2:
            # intermediate node
            nodes_to_reduce.append(node)
        # else: a branch node; do not reduce
    for node in nodes_to_remove:
        edge = next(iter(graph[node].values()))
        other_node = edge.next_node
        other_facing = opposite_facing(edge.facing)
        if other_node not in graph:
            continue
        del graph[other_node][other_facing]
        del graph[node]
        reduced = True
    for node in nodes_to_reduce:
        edges = list(graph[node].items())
        if len(edges) < 2:
            # one of the end nodes already removed.
            # this node will be removed in the next
            # iteration, so we can skip it now
            continue
        assert len(edges) == 2
        facing_N_to_A, edge_N_to_A = edges[0]
        facing_N_to_B, edge_N_to_B = edges[1]
        A = edge_N_to_A.next_node
        B = edge_N_to_B.next_node
        facing_A_to_N = opposite_facing(edge_N_to_A.facing)
        facing_B_to_N = opposite_facing(edge_N_to_B.facing)
        # Replace pair of edges A -> node -> B with direct A -> B
        edge_A_to_N = graph[A][facing_A_to_N]
        assert edge_A_to_N.next_node == node
        edge_A_to_N.next_node = B
        edge_A_to_N.score = edge_A_to_N.score + edge_N_to_B.score + get_turn_penalty(edge_A_to_N.facing, facing_N_to_B)
        edge_A_to_N.facing = edge_N_to_B.facing
        edge_A_to_N.steps.update(edge_N_to_B.steps)

        # Replace pair of edges B -> node -> A with direct B -> A
        edge_B_to_N = graph[B][facing_B_to_N]
        assert edge_B_to_N.next_node == node
        edge_B_to_N.next_node = A
        edge_B_to_N.score = edge_B_to_N.score + edge_N_to_A.score + get_turn_penalty(edge_B_to_N.facing, facing_N_to_A)
        edge_B_to_N.facing = edge_N_to_A.facing
        edge_B_to_N.steps.update(edge_N_to_A.steps)

        del graph[node]
        reduced = True
    return reduced


def find_best_paths(graph, start, end):
    best_paths = []
    best_score = None
    facing = 0
    q = []
    min_scores = {(start[0], start[1], facing): 0}
    heapq.heappush(q, (0, start, facing, [start]))
    while q:
        score, current, facing, path = heapq.heappop(q)
        if best_score is not None and score > best_score:
            # cannot beat best path any more
            break
        if current == end:
            if best_score is None or score < best_score:
                best_score = score
                best_paths = []
            if score == best_score:
                best_paths.append(path)
        key = (current[0], current[1], facing)
        if key in min_scores and min_scores[key] < score:
            continue
        min_scores[key] = score
        assert current in graph, f"Node {current} not in graph"
        for n_facing, edge in graph[current].items():
            if edge.next_node in path:
                # no cycles allowed
                continue
            turn_penalty = get_turn_penalty(facing, n_facing)
            heapq.heappush(q, (
                score + turn_penalty + edge.score,
                edge.next_node,
                edge.facing,
                path[:] + [edge.next_node]
            ))
    return best_score, best_paths


def print_edge_stats(graph):
    edges = {0:0, 1:0, 2:0, 3:0, 4:0}
    for k in graph.values():
        edges[len(k)] += 1
    print(f"Edge stats: {edges}")


def part1(input):
    g = Grid(input.get_valid_lines())
    # Slow solution:
    #start = find_position(g, 'S')
    #end = find_position(g, 'E')
    #return shortest_dfs(g, start, end)

    start, end, nodes = find_nodes(g)
    connections = make_smaller_graph(g, nodes)
    #print_edge_stats(connections)
    while reduce_dead_ends(connections, start, end):
        #print_edge_stats(connections)
        pass
    #print(f"Graph size: {len(connections)}")
    assert start in connections
    score, _ = find_best_paths(connections, start, end)
    return score


e.run_tests(1, part1)
e.run_main(1, part1)


def expand_positions(positions, graph, path):
    for i in range(len(path) - 1):
        A = path[i]
        B = path[i+1]
        # leg from A to B
        # Beware, there can be multiple edges from A starting in different directions
        # and all leading to B, but we only want the shortest one.
        edges_A_to_B = []
        for edge in graph[A].values():
            if edge.next_node == B:
                heapq.heappush(edges_A_to_B, (edge.score, edge.steps))
        assert edges_A_to_B, f"Edge from {A} to {B} not found"
        best_score = None
        while edges_A_to_B:
            score, steps = heapq.heappop(edges_A_to_B)
            if best_score is not None and best_score < score:
                break
            best_score = score
            positions.update(steps)


def print_positions(g, positions):
    for r in range(g.h):
        line = []
        for c in range(g.w):
            if (r, c) in positions:
                line.append('O')
            else:
                line.append(g.get(r, c))
        print(f'{str(r).rjust(3, " ")} ' + ''.join(line))


def print_graph(graph):
    def fac_sym(f):
        return '>^<v'[f]
    for node, x in graph.items():
        print(f"Node {node}")
        for f, e in x.items():
            print(f"  {fac_sym(f)} {e.next_node} - score {e.score}, facing {fac_sym(e.facing)}")


def part2(input):
    g = Grid(input.get_valid_lines())
    start, end, nodes = find_nodes(g)
    connections = make_smaller_graph(g, nodes)
    #print(f"Graph size: {len(connections)}")
    #print_graph(connections)
    #print_edge_stats(connections)
    while reduce_dead_ends(connections, start, end):
        #print_edge_stats(connections)
        pass
    #print(f"Graph size: {len(connections)}")
    #print_graph(connections)
    assert start in connections
    _, paths = find_best_paths(connections, start, end)
    positions = set([start])
    for path in paths:
        expand_positions(positions, connections, path)
    #print_positions(g, set())
    #print()
    print_positions(g, positions)
    return len(positions)


e.run_tests(2, part2)
e.run_main(2, part2)

# 727 too high
