#!/usr/bin/python3.12

from collections import defaultdict, deque
import re


def parse_input(full_input):
    lines = [ln.strip() for ln in full_input.split("\n") if ln.strip()]
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


def get_terminals(subs, formula):
    atom_re = re.compile(r'[A-Z][a-z]*')
    def split_formula(form):
        tokens = atom_re.findall(form)
        return set(tokens)
    formula_tokens = split_formula(formula)
    non_terminals = set(subs.keys())
    terminals = formula_tokens - non_terminals
    # assumption - all rules' right sides only contain terminals and non-terminals found in the final formula
    #   ^ does not hold - there are some intermediate non-terminals
    # assumption - all atoms of the final formula are provided by at least one rule's right side
    # verify assumptions
    rule_atoms = set()
    for rules in subs.values():
        for rule in rules:
            tokens = split_formula(rule)
            #assert formula_tokens.issuperset(tokens), f"formula {formula_tokens}, tokens {tokens}"
            rule_atoms.update(tokens)
    assert rule_atoms.issuperset(formula_tokens)

    return terminals, non_terminals


def part2(full_input):
    # Context-free grammar
    # Assumption: all formulas made up of atoms
    #    each atom starts with capital letter -> tokenization
    # Find terminals and non-terminals
    # Is the grammar LL1?
    # Construct First and Follow sets
    # Parse formula using backtracking, get abstract tree, count its nodes
    subs, formula = parse_input(full_input)
    terminals, nonterminals = get_terminals(subs, formula)
    print(f"terminals: {terminals}")
    print(f"non terminals: {nonterminals}")
    return 0


def main():
    with open("input19.txt", "rt") as f:
        main_input = f.read()
    test_inputs = [("""e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""", 7, 6)]
    # test cases
    num = 1
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
