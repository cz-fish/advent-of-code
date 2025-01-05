#!/usr/bin/python3.12

from pyaoc import Env

from collections import defaultdict, deque
import heapq
import re


e = Env(19)
e.T("""e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""", 7, 6)


def parse_input(full_input):
    lines = full_input.get_valid_lines()
    transforms = defaultdict(list)
    formula = lines.pop()
    for ln in lines:
        assert " => " in ln
        source, dest = ln.split(" => ")
        transforms[source].append(dest)
    return transforms, formula


def part1(full_input):
    subs, formula = parse_input(full_input)
    options = set()
    for needle in subs.keys():
        start = 0
        while True:
            where = formula.find(needle, start)
            if where == -1:
                break
            prefix = formula[:where]
            suffix = formula[where + len(needle):]
            for r in subs[needle]:
                candidate = prefix + r + suffix
                options.add(candidate)
            start = where + 1
    return len(options)


e.run_tests(1, part1)
e.run_main(1, part1)


def num_transforms(rev_subs, formula):
    q = deque([(formula, 0)])
    seen = set([formula])
    counter = 0
    max_depth = 0
    shortest = len(formula)
    while q:
        form, depth = q.popleft()

        counter += 1
        max_depth = max(max_depth, depth)
        shortest = min(shortest, len(form))
        if counter % 1000 == 0:
            print(f"counter {counter}, max_depth {max_depth}, shortest {shortest}")

        if form == 'e':
            return depth

        for right, sub in rev_subs.items():
            start = 0
            while True:
                where = form.find(right, start)
                if where == -1:
                    break
                reduced = form[:where] + sub + form[where + len(right):]
                if reduced not in seen:
                    seen.add(reduced)
                    q.append((reduced, depth + 1))
                start = where + 1
    assert False, "Solution not found"


def part2_a(full_input):
    # BFS through all possible reductions.
    # Too slow, queue grows too quickly
    subs, formula = parse_input(full_input)
    reverse = {}
    for left, rights in subs.items():
        for right in rights:
            assert right not in reverse, f"'{right}' has two left sides: '{left}' and '{reverse[right]}'"
            reverse[right] = left
    return num_transforms(reverse, formula)


_atom_re = re.compile(r'[A-Z][a-z]*')


def tokenize(formula):
    return list(_atom_re.findall(formula))


def get_terminals(subs, formula):
    formula_tokens = set(tokenize(formula))
    non_terminals = set(subs.keys())
    terminals = formula_tokens - non_terminals
    # assumption - all rules' right sides only contain terminals and non-terminals found in the final formula
    #   ^ does not hold - there are some intermediate non-terminals
    # assumption - all atoms of the final formula are provided by at least one rule's right side
    # verify assumptions
    rule_atoms = set()
    for rules in subs.values():
        for rule in rules:
            tokens = set(tokenize(rule))
            #assert formula_tokens.issuperset(tokens), f"formula {formula_tokens}, tokens {tokens}"
            rule_atoms.update(tokens)
    assert rule_atoms.issuperset(formula_tokens)

    return terminals, non_terminals


def make_rule_map(rules):
    firsts = {}
    for left in rules.keys():
        possible_first = {}
        q = deque()
        for rule in rules[left]:
            tokens, rule_nr = rule
            q.append((tokens[0], rule_nr))
        while q:
            head, first_rule = q.popleft()
            if head in possible_first:
                possible_first[head].add(first_rule)
            else:
                possible_first[head] = set([first_rule])
                if head in rules:
                    for next_rule in rules[head]:
                        tokens, _ = next_rule
                        q.append((tokens[0], first_rule))
        firsts[left] = possible_first
    #for k, v in firsts.items():
    #    print(f"{k} ->")
    #    for o, r in v.items():
    #        print(f"      {o} via {r}")
    return firsts
"""
    # map: for each left side - a list of different possible right side expansions
    #      for each expansion: (the first atom, the rest, and number of steps, list of numbers of rules applied)
    rule_map = {}
    for left, rights in rules.items():
        expansions = []
        firsts = set()
        for rule, number in rights:
            expansions.append((rule[0], rule[1:], 1, [number]))
            firsts.add(rule[0])
        rule_map[left] = (expansions, firsts)

    # TODO: this somehow has to be done transitively
    lefts = set(rule_map.keys())
    transitive_map = defaultdict(set)
    for left in lefts:
        transitive_map[left] = set(rule_map[left][1])
    change = True
    while change:
        change = False
        for left in lefts:
            new_set = set(transitive_map[left])
            for first in transitive_map[left]:
                if first not in transitive_map:
                    continue
                new_set.update(transitive_map[first])
            if transitive_map[left] != new_set:
                transitive_map[left] = new_set
                change = True
    for left, firsts in transitive_map.items():
        print(f"Firsts of {left}: {list(firsts)}")
    return rule_map
"""


def check_and_append(q, seen, formula, exp, depth, pos):
    if len(exp) > len(formula):
        return
    if pos == len(formula) and exp:
        return
    #heapq.heappush(q, (depth, depth, exp, pos))
    key = (pos, tuple(exp))
    if key in seen:
        return
    seen.add(key)
    q.append((exp, depth, pos))


def count_rule_expansions(rule_map, rule_by_nr, formula):
    q = deque()
    # current expansion, depth, formula_pos
    q.append((["e"], 0, 0))
    #q = []
    # -pos, depth, expansion, pos
    #heapq.heappush(q, (0, 0, ["e"], 0))
    best = 0
    counter = 0
    seen = set()
    while q:
        exp, depth, pos = q.popleft()
        #_, depth, exp, pos = heapq.heappop(q)
        counter += 1
        best = max(best, pos)
        if counter % 10000 == 0:
            print(f"{counter}: best pos {best}, depth {depth}, q len {len(q)}")
        if pos == len(formula):
            if not exp:
                # solution reached
                return depth
            # over-expanded
            continue
        if not exp:
            # exhausted all expansion, but no solution matched
            continue
        if len(exp) >= len(formula):
            # already too long, no need to continue, as every
            # expansion rule only makes the formula longer
            continue
        first = exp[0]
        peek = formula[pos]
        if first == peek:
            # possible to consume one character
            #q.append((exp[1:], depth, pos + 1))
            check_and_append(q, seen, formula, exp[1:], depth, pos + 1)
        if first not in rule_map or peek not in rule_map[first]:
            # not possible to expand
            continue
        # expand all potentially perspective rules
        for rule_nr in rule_map[first][peek]:
            rule_tokens = rule_by_nr[rule_nr]
            #q.append((rule_tokens + exp[1:], depth + 1, pos))
            check_and_append(q, seen, formula, rule_tokens + exp[1:], depth + 1, pos)

    assert False, "Solution not found"


def reduce_formula(formula, rules):
    q = []
    best = {}
    heapq.heappush(q, (len(formula), 0, formula))
    counter = 0
    shortest = None
    while q:
        size, depth, f = heapq.heappop(q)
        if f == 'e':
            break
        if shortest is None or size < shortest:
            shortest = size
        counter += 1
        if counter % 1000 == 0:
            print(f"{counter} {size} / {shortest}, {len(q)}")
        for l, rights in rules.items():
            for r in rights:
                i = f.find(r)
                if i == -1:
                    continue
                nf = f[:i] + l + f[i+len(r):]
                if nf in best:
                    if best[nf] <= depth + 1:
                        continue
                best[nf] = depth + 1
                heapq.heappush(q, (len(nf), depth + 1, nf))
    return best['e']


def part2(full_input):
    subs, formula = parse_input(full_input)

    # tokenize all rules, and give them all unique numbers
    # Assumption: all formulas made up of atoms
    #    each atom starts with capital letter -> tokenization
    rule_by_left = {}
    rule_by_id = {}
    counter = 0
    for left, rights in subs.items():
        rules_of_left = []
        for right in rights:
            tokenized = tokenize(right)
            rules_of_left.append((tokenized, counter))
            rule_by_id[counter] = tokenized
            counter += 1
        rule_by_left[left] = rules_of_left
    token_formula = tokenize(formula)

    # Find terminals and non-terminals -> not really that useful because the formula doesn't only contain
    #    terminals, but some non-terminals, too.
    #terminals, nonterminals = get_terminals(subs, formula)
    #print(f"terminals: {terminals}")
    #print(f"non terminals: {nonterminals}")

    # Is the grammar LL1? Does it matter?

    # Construct First and Follow sets
    # map: for each non-terminal a list of firsts. For each first in the list - full expansion from the non-terminal and number of steps
    #rule_map = make_rule_map(rule_by_left)

    # Parse formula using prefix matching. We should be able to accumulate number of rules applied as we go
    #return count_rule_expansions(rule_map, rule_by_id, token_formula)

    return reduce_formula(formula, subs)


e.run_tests(2, part2)
e.run_main(2, part2)
