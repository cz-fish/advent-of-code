#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict

e = Env(23)
e.T("""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""", 7, "co,de,ka,ta")


def make_dual_connections(lines):
    conn = defaultdict(set)
    for ln in lines:
        first, second = ln.split('-')
        conn[first].add(second)
        conn[second].add(first)
    return conn


def find_groups_of_three_with_t(conn):
    triangles = []
    for first in conn.keys():
        if first[0] != 't':
            continue
        seconds = list(conn[first])
        for i, second in enumerate(conn[first]):
            if second[0] == 't':
                # Make sure not to count a group with two 't's twice
                if second > first:
                    continue
            for j in range(i + 1, len(seconds)):
                third = seconds[j]
                if third[0] == 't':
                    if third > first:
                        continue
                if third not in conn[second]:
                    continue
                triangles.append((first, second, third))
    return triangles


def part1(input):
    conn = make_dual_connections(input.get_valid_lines())
    return len(find_groups_of_three_with_t(conn))


e.run_tests(1, part1)
e.run_main(1, part1)


def bronKerbosch(r, p, x, conn, cliques):
    if not p and not x:
        cliques.append(','.join(sorted(list(r))))
        return
    p_list = list(p)
    for v in p_list:
        n_p = set([u for u in p if u in conn[v]])
        n_x = set([u for u in x if u in conn[v]])
        r.add(v)
        bronKerbosch(r, n_p, n_x, conn, cliques)
        r.remove(v)
        p.remove(v)
        x.add(v)


def max_clique(conn):
    cliques = []
    r = set()
    p = set(conn.keys())
    x = set()
    bronKerbosch(r, p, x, conn, cliques)
    cliques.sort(key=lambda x: -len(x))
    return cliques[0]


def part2(input):
    conn = make_dual_connections(input.get_valid_lines())
    return max_clique(conn)


e.run_tests(2, part2)
e.run_main(2, part2)
