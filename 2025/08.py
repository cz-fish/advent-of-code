#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict, deque, Counter

e = Env(8, param=1000)
e.T("""162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""", 40, 25272, param=10)


def parse_input(input):
    points = []
    for ln in input.get_valid_lines():
        coords = ln.split(',')
        assert len(coords) == 3
        points.append(tuple([int(x) for x in coords]))
    return points


def calculate_distances(points):
    dists = []
    for i, p in enumerate(points):
        for j in range(i + 1, len(points)):
            q = points[j]
            dx = p[0] - q[0]
            dy = p[1] - q[1]
            dz = p[2] - q[2]
            dist = dx*dx + dy*dy + dz*dz
            dists.append((dist, i, j))
    return dists


def make_connections(dists, iterations):
    components = 0
    connections = {}
    merge_comps = defaultdict(set)
    for i in range(iterations):
        _, a, b = dists[i]
        # connect points a and b
        if a in connections:
            a_con = connections[a]
            if b in connections:
                b_con = connections[b]
                # merge groups of a and of b
                merge_comps[a_con].add(b_con)
                merge_comps[b_con].add(a_con)
            else:
                # Add b to group of a
                connections[b] = a_con
        elif b in connections:
            b_con = connections[b]
            # Add a to group of b
            connections[a] = b_con
        else:
            # New group
            connections[a] = components
            connections[b] = components
            components += 1
    return connections, merge_comps


def merge_groups(grouping, todo_merge):
    merged = set()
    number = 0
    new_numbers = {}
    for g in todo_merge.keys():
        if g in merged:
            continue
        q = deque([g])
        while q:
            x = q.popleft()
            if x in merged:
                continue
            new_numbers[x] = number
            merged.add(x)
            if x in todo_merge:
                for v in todo_merge[x]:
                    q.append(v)
        number += 1
    for k, v in grouping.items():
        if v in new_numbers:
            grouping[k] = new_numbers[v]
        else:
            new_numbers[v] = number
            grouping[k] = number
            number += 1
    


def part1(input):
    points = sorted(parse_input(input))
    dists = calculate_distances(points)
    dists.sort()
    iterations = e.get_param()
    #print(dists)
    #print(len(dists), iterations)
    assert iterations <= len(dists)
    grouping, todo_merge = make_connections(dists, iterations)
    #print("---")
    #for k, v in grouping.items():
    #    print(k, v)
    #print("---")
    #for k, v in todo_merge.items():
    #    print(k, v)
    merge_groups(grouping, todo_merge)
    #print("---")
    #for k, v in grouping.items():
    #    print(k, v)
    group_counter = Counter(grouping.values())
    group_sizes = sorted(group_counter.values(), reverse=True)
    assert len(group_sizes) >= 3
    #print(group_sizes)
    return group_sizes[0] * group_sizes[1] * group_sizes[2]


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    points = sorted(parse_input(input))
    dists = calculate_distances(points)
    dists.sort()
    groups = defaultdict(set)
    point_map = {}
    for i in range(len(points)):
        point_map[i] = i
        groups[i].add(i)
    connection = 0
    while len(groups) > 1:
        assert connection < len(dists)
        _, a, b = dists[connection]
        connection += 1
        g_a = point_map[a]
        g_b = point_map[b]
        if g_a == g_b:
            # already in the same gorup, no change
            continue
        g_merged = min(g_a, g_b)
        g_other = max(g_a, g_b)
        point_map[a] = g_merged
        point_map[b] = g_merged
        groups[g_merged].add(g_a)
        groups[g_merged].add(g_b)
        for x in groups[g_other]:
            groups[g_merged].add(x)
            point_map[x] = g_merged
        del groups[g_other]
    connection -= 1
    _, i, j = dists[connection]
    return points[i][0] * points[j][0]


e.run_tests(2, part2)
e.run_main(2, part2)
