#!/usr/bin/python3.8

from aoc import Env
from collections import deque
import re

e = Env(19)
e.T("""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""", 2, None)
e.T("""42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""", 3, 12)
e.T("""8: 42
11: 42 31
42: "a"
31: "b"
0: 11

aab
aabb
abb
""", 0, 1)


def parse_rules(rules):
    term = {}
    nonterm = {}
    for rule in rules:
        m = re.match(r'^(\d+): (.*)', rule)
        assert m is not None

        nr = int(m.group(1))
        p = m.group(2)

        if '"' in p:
            m = re.match(r'"(.*)"', p)
            term[nr] = m.group(1)
            continue

        parts = p.split('|')
        options = []
        for pt in parts:
            options += [[int(x) for x in re.findall(r'\d+', pt)]]
        nonterm[nr] = options
    return term, nonterm


def make_rule0_regex_for_pt1(rules):
    term, nonterm = parse_rules(rules)

    while 0 not in term:
        comp = set(term.keys())
        for nr, opts in nonterm.items():
            if nr in term:
                continue
            parts = []
            for o in opts:
                if all([i in comp for i in o]):
                    parts += [''.join([term[i] for i in o])]
                else:
                    break
            else:
                s = '|'.join(parts)
                if len(parts) > 1:
                    s = f"({s})"
                term[nr] = s
                comp.add(nr)
    return term[0]


def part1_regex(input):
    # Alternative approach with regexes
    #   works well for part 1 but hard to expand for part 2
    gr = input.get_groups()
    rules = gr[0]
    messages = gr[1]
    rule0 = make_rule0_regex_for_pt1(rules)
    r = re.compile(f"^{rule0}$")
    valid = [msg for msg in messages if r.match(msg)]
    return len(valid)


e.run_tests(1, part1_regex)
e.run_main(1, part1_regex)


def replace_rules_for_pt2(nonterm):
    nonterm[8] = [[42], [42, 8]]
    nonterm[11] = [[42, 31], [42, 11, 31]]


def msg_valid(msg, term, nonterm):
    q = deque()
    q.append((0,[0]))
    while q:
        index, rules = q.popleft()
        rule = rules[0]
        if rule in term:
            if msg[index] == term[rule]:
                # character matched
                index += 1
                if index == len(msg):
                    # at the end of the msg. Did we satisfy all rules?
                    if len(rules) == 1:
                        return True
                    # else rules not satisfied
                else:
                    if len(rules) > 1:
                        q.append((index, rules[1:]))
            # else no match
        else:
            for opts in nonterm[rule]:
                q.append((index, opts + rules[1:]))
    # all branches exhausted and no match
    return False


def part1(input):
    gr = input.get_groups()
    term, nonterm = parse_rules(gr[0])
    messages = gr[1]
    valid = [msg for msg in messages if msg_valid(msg, term, nonterm)]
    return len(valid)


def part2(input):
    gr = input.get_groups()
    term, nonterm = parse_rules(gr[0])
    replace_rules_for_pt2(nonterm)
    messages = gr[1]
    valid = [msg for msg in messages if msg_valid(msg, term, nonterm)]
    return len(valid)


e.run_tests(1, part1)
e.run_main(1, part1)
e.run_tests(2, part2)
e.run_main(2, part2)
