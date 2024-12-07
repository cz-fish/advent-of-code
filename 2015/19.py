#!/usr/bin/python3.12

from pyaoc import Env

from collections import defaultdict, deque
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


def count_rule_expansions(rule_map, formula):
    return 0


def part2(full_input):
    subs, formula = parse_input(full_input)

    # tokenize all rules, and give them all unique numbers
    # Assumption: all formulas made up of atoms
    #    each atom starts with capital letter -> tokenization
    rules = {}
    counter = 0
    for left, rights in subs.items():
        rules_of_left = []
        for right in rights:
            rules_of_left.append((tokenize(right), counter))
            counter += 1
        rules[left] = rules_of_left
    token_formula = tokenize(formula)

    # Find terminals and non-terminals -> not really that useful because the formula doesn't only contain
    #    terminals, but some non-terminals, too.
    #terminals, nonterminals = get_terminals(subs, formula)
    #print(f"terminals: {terminals}")
    #print(f"non terminals: {nonterminals}")

    # Is the grammar LL1? Does it matter?

    # Construct First and Follow sets
    # map: for each non-terminal a list of firsts. For each first in the list - full expansion from the non-terminal and number of steps
    rule_map = make_rule_map(rules)

    # Parse formula using prefix matching. We should be able to accumulate number of rules applied as we go
    return count_rule_expansions(rule_map, token_formula)


e.run_tests(2, part2)
e.run_main(2, part2)


"""
    for test_case, exp1, exp2 in test_inputs:
        res = part1(test_case)
        print(f"Test case {num}, part 1, expected {exp1} got {res} {'not a ' if res != exp1 else ''}match")
        res = part2(test_case)
        print(f"Test case {num}, part 2, expected {exp2} got {res} {'not a ' if res != exp2 else ''}match")
        num += 1
    # actual input
    print(f"Actual input, part 1: {part1(main_input)}")
    print(f"Actual input, part 2: {part2(main_input)}")


if __name__ == "__main__":
    main()
"""
