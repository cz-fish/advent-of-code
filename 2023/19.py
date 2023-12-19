#!/usr/bin/python3.8

from aoc import Env
from dataclasses import dataclass
from collections import deque

e = Env(19)
e.T("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""", 19114, 167409079868000)

e.T("""in{x<2001:A,R}

{x=1,m=1,a=1,s=1}""", None, 2000 * 4000 * 4000 * 4000)

e.T("""in{x<4000:R,m<4000:R,a<4000:R,s<4000:R,A}

{x=1,m=1,a=1,s=1}""", None, 1)


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


def parse_workflows(lines):
    workflows = {}
    for ln in lines:
        bracket = ln.index('{')
        name = ln[:bracket]
        assert ln.endswith('}')
        rule_str = ln[bracket+1:-1]
        rules = []
        for term in rule_str.split(','):
            if ':' in term:
                cond, dest = term.split(':')
                if '>' in cond:
                    var, val = cond.split('>')
                    rel = '>'
                else:
                    var, val = cond.split('<')
                    rel = '<'
                rules.append((var, rel, int(val), dest))
            else:
                # last rule
                rules.append(('last', term))
        assert rules
        assert rules[-1][0] == 'last'
        workflows[name] = rules
    return workflows


def parse_parts(lines):
    parts = []
    for ln in lines:
        assert ln.startswith('{') and ln.endswith('}')
        ln = ln[1:-1]
        terms = ln.split(',')
        t = {}
        for term in terms:
            k, v = term.split('=')
            assert k not in t
            assert k in 'xmas'
            t[k] = int(v)
        parts.append(Part(x=t['x'], m=t['m'], a=t['a'], s=t['s']))
    return parts


def parse_input(input):
    groups = input.get_groups()
    assert len(groups) == 2
    workflows = parse_workflows(groups[0])
    parts = parse_parts(groups[1])
    return workflows, parts


def run_workflow(workflow, part):
    for rule in workflow:
        if len(rule) == 2:
            assert rule[0] == 'last'
            return rule[1]
        assert len(rule) == 4
        var, rel, val, state = rule
        if var == 'x':
            test = part.x
        elif var == 'm':
            test = part.m
        elif var == 'a':
            test = part.a
        elif var == 's':
            test = part.s
        else:
            assert False
        if (rel == '>' and test > val) or (rel == '<' and test < val):
            return state
    assert False


def process_parts_through_workflows(workflows, parts, start):
    q = deque()
    for part in parts:
        q.append((part, start))
    accepted = []
    while q:
        part, workflow = q.popleft()
        state = run_workflow(workflows[workflow], part)
        if state == 'A':
            accepted.append(part)
        elif state != 'R':
            q.append((part, state))
    return accepted


def part1(input):
    workflows, parts = parse_input(input)
    accepted = process_parts_through_workflows(workflows, parts, 'in')
    return sum([p.x + p.m + p.a + p.s for p in accepted])


def try_workflows(workflows, start):
    q = deque()
    q.append((Part(x=0, m=0, a=0, s=0), Part(x=4001, m=4001, a=4001, s=4001), start))
    accepted = []
    rejected = []
    while q:
        lower, upper, flow = q.popleft()
        #print(lower, upper, flow)
        if flow == 'R':
            rejected.append((lower, upper))
            continue
        if flow == 'A':
            accepted.append((lower, upper))
            continue
        rules = workflows[flow]
        for rule in rules:
            if len(rule) == 4:
                # standard rule
                var, rel, val, state = rule
                test_lower = getattr(lower, var)
                test_upper = getattr(upper, var)
                if (rel == '>' and test_upper <= val) or (rel == '<' and test_lower >= val):
                    # cannot pass; skip rule
                    pass
                elif (rel == '>' and test_lower > val) or (rel == '<' and test_upper < val):
                    # always passes; no need to adjust intervals and break after this rule
                    q.append((lower, upper, state))
                    break
                else:
                    # passes for some interval; adjust interval
                    new_lower = Part(x=lower.x, m=lower.m, a=lower.a, s=lower.s)
                    new_upper = Part(x=upper.x, m=upper.m, a=upper.a, s=upper.s)
                    if rel == '>':
                        # The subinterval where lower > val goes to next state
                        # The subinterval where upper <= val goes to next rule
                        setattr(new_lower, var, val)
                        q.append((new_lower, new_upper, state))
                        setattr(upper, var, val + 1)
                    else:
                        # The subinterval where upper < val goes to next state
                        # The subinterval where lower >= val goes to next rule
                        setattr(new_upper, var, val)
                        q.append((new_lower, new_upper, state))
                        setattr(lower, var, val - 1)
            else:
                # last rule; always passes
                state = rule[1]
                q.append((lower, upper, state))
    return accepted, rejected

### -- Unnecessary code. Intervals cannot overlap

def interval_overlap(a_min, a_max, b_min, b_max):
    if a_max <= b_min or a_min >= b_max:
        # no overlap
        return -1, -1
    if a_min >= b_min and a_min <= b_max:
        over_start = a_min
    elif b_min >= a_min and b_min <= a_max:
        over_start = b_min
    if a_max >= b_min and a_max <= b_max:
        over_end = a_max
    elif b_max >= a_min and b_max <= a_max:
        over_end = b_max
    return over_start, over_end

# pytest
def test_interval_overlap():
    assert interval_overlap(0, 3, 5, 10) == (-1, -1)
    assert interval_overlap(0, 3, 3, 6) == (-1, -1)
    assert interval_overlap(3, 6, 0, 3) == (-1, -1)
    assert interval_overlap(5, 9, 5, 9) == (5, 9)
    assert interval_overlap(5, 9, 6, 7) == (6, 7)
    assert interval_overlap(0, 6, 3, 9) == (3, 6)
    assert interval_overlap(2, 8, 3, 9) == (3, 8)


def unoverlap_intervals(intervals):
    order = 'xmas'
    for i, interval in enumerate(intervals):
        print(i, interval)
    for i, first in enumerate(intervals):
        for j in range(i+1, len(intervals)):
            second = intervals[j]
            overlap_from = [-1, -1, -1, -1]
            overlap_to = [-1, -1, -1, -1]
            for k, x in enumerate(order):
                first_lower = getattr(first[0], x)
                first_upper = getattr(first[1], x)
                second_lower = getattr(second[0], x)
                second_upper = getattr(second[1], x)
                over_from, over_to = interval_overlap(first_lower, first_upper, second_lower, second_upper)
                overlap_from[k] = over_from
                overlap_to[k] = over_to
            if all([o > -1 for o in overlap_from]):
                # overlap in all 4 variables
                print(f"Overlap between {i} and {j}: {overlap_from} {overlap_to}")
                # TODO: reduce one of the intervals


### -- end Unnecessary code

def interval_size(intervals):
    total = 0
    def d(high, low):
        return high - low - 1
    for lower, upper in intervals:
        rng = d(upper.x, lower.x) * d(upper.m, lower.m) * d(upper.a, lower.a) * d(upper.s, lower.s)
        total += rng
    return total


def part2(input):
    workflows, _ = parse_input(input)
    accepted, rejected = try_workflows(workflows, 'in')
    a_size = interval_size(accepted)
    r_size = interval_size(rejected)
    assert a_size + r_size == 4000 * 4000 * 4000 * 4000
    #print(f"accepted {a_size}, rejected {r_size}, total {a_size + r_size}")
    return a_size


if __name__ == '__main__':
    e.run_tests(1, part1)
    e.run_main(1, part1)

    e.run_tests(2, part2)
    e.run_main(2, part2)
