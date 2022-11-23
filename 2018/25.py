#!/usr/bin/python3.8

from aoc import Env
from collections import deque

e = Env(25)
e.T(""" 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""", 2, None)
e.T(""" 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0
 6,0,0,0""", 1, None)
e.T("""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""", 4, None)
e.T("""1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""", 3, None)
e.T("""1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""", 8, None)


LIMIT = 3


def get_points(lines):
    pts = []
    for ln in lines:
        pts.append([int(p) for p in ln.split(',')])
    return pts


def dist(A, B):
    return sum([abs(A[i] - B[i]) for i in range(len(A))])


def make_graph(points):
    graph = {i: [] for i in range(len(points))}
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if dist(points[i], points[j]) <= LIMIT:
                graph[i].append(j)
                graph[j].append(i)
    return graph


def visit_component(graph, start, visited):
    q = deque()
    q.append(start)
    while q:
        pos = q.pop()
        if pos in visited:
            continue
        visited.add(pos)
        for con in graph[pos]:
            if con not in visited:
                q.append(con)


def count_components(graph):
    counter = 0
    visited = set()
    for start in graph.keys():
        if start in visited:
            continue
        counter += 1
        visit_component(graph, start, visited)
    return counter


def part1(input):
    points = get_points(input.get_valid_lines())
    graph = make_graph(points)
    return count_components(graph)


e.run_tests(1, part1)
e.run_main(1, part1)

