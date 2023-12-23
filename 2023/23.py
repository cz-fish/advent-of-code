#!/usr/bin/python3.8

from aoc import Env, Grid
from collections import deque, defaultdict

e = Env(23)
e.T("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""", 94, 154)


DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

STEP = {
    DOWN: (1, 0),
    RIGHT: (0, 1),
    UP: (-1, 0),
    LEFT: (0, -1),
}

SLOPES = {
    '>': RIGHT,
    '^': UP,
    '<': LEFT,
    'v': DOWN,
}


def find_paths(grid, start, ignore_slope=False):
    end = None
    edges = []
    nodes = set()
    nodes.add(start)
    q = deque()
    q.append((start, DOWN, 0, False, start))
    while q:
        pos, heading, dist, slopes, prev = q.popleft()
        row, col = pos
        row += STEP[heading][0]
        col += STEP[heading][1]
        dist += 1
        if row == grid.h - 1:
            # End reached
            if end is not None:
                assert end == (row, col)
            end = (row, col)
            nodes.add(end)
            edges.append((prev, end, dist, slopes))
            continue
        c = grid.get(row, col)
        if c in SLOPES and heading != SLOPES[c]:
            # Going wrong way across a slope, abort path
            continue
        elif c in SLOPES:
            # Passed a slope in the correct direction
            slopes = True
        exits = [d for d in [DOWN, RIGHT, UP, LEFT] if grid.get(row + STEP[d][0], col + STEP[d][1]) != '#']
        assert len(exits) > 1, f"Dead end found at ({row}, {col})"
        came_from = (heading + 2) % 4
        assert came_from in exits, f"Direction we came from isn't in exits. {row}, {col}, {came_from}, {exits}"
        other_exits = [e for e in exits if e != came_from]
        assert len(other_exits) >= 1
        if len(other_exits) >= 2:
            #print(f"crossroad {row}, {col}, exits: {other_exits}")
            # crossroads
            node = (row, col)
            # record edge
            edges.append((prev, node, dist, slopes))
            if node in nodes:
                # We've already been in this node, no need to redo
                continue
            nodes.add(node)
            for exit in other_exits:
                q.append(((row, col), exit, 0, False, node))
        else:
            # Continue forward through the path
            heading = other_exits[0]
            q.append(((row, col), heading, dist, slopes, prev))
    graph = defaultdict(list)
    for edge in edges:
        #print(edge)
        edge_from, edge_to, dist, has_slopes = edge
        graph[edge_from].append((edge_to, dist))
        if not has_slopes or ignore_slope:
            graph[edge_to].append((edge_from, dist))
    return graph, end


def longest_path_through_graph(graph, start, end):
    max_len = 0
    q = deque([(start, 0, [])])
    while q:
        node, dist, visited = q.popleft()
        if node == end:
            max_len = max(max_len, dist)
            continue
        for nei, d in graph[node]:
            if nei not in visited:
                q.append((nei, dist + d, visited + [node]))
    return max_len

def print_map(grid, graph):
    for row in range(grid.h):
        line = ''
        for col in range(grid.w):
            if grid.get(row, col) == '#':
                line += '#'
            elif (row, col) in graph:
                line += 'O'
            else:
                line += ' '
        print(line)


def part1(input):
    grid = Grid(input.get_valid_lines())
    start = 0, grid.grid[0].index('.')
    graph, end = find_paths(grid, start)
    #print_map(grid, graph)
    return longest_path_through_graph(graph, start, end)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    grid = Grid(input.get_valid_lines())
    start = 0, grid.grid[0].index('.')
    graph, end = find_paths(grid, start, ignore_slope=True)
    return longest_path_through_graph(graph, start, end)


e.run_tests(2, part2)
e.run_main(2, part2)
