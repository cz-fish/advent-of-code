#!/usr/bin/python3.12

from pyaoc import Env
from collections import defaultdict

e = Env(5)
e.T("""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""", 143, 123)


def parse_rules(rules):
    befores = defaultdict(set)
    afters = defaultdict(set)
    for r in rules:
        bef, aft = [int(x) for x in r.split('|')]
        befores[aft].add(bef)
        afters[bef].add(aft)
    return befores, afters


def lines_good_and_bad(lines, befores):
    goods = []
    bads = []
    for ln in lines:
        numbers = [int(x) for x in ln.split(',')]
        assert len(numbers) % 2 == 1, f"Line length not odd; doesn't have a middle. {numbers}"
        good = True
        for i, num in enumerate(numbers):
            for j in range(i+1, len(numbers)):
                if numbers[j] in befores[num]:
                    good = False
                    break
            if not good:
                break
        if good:
            goods.append(numbers)
        else:
            bads.append(numbers)
    return goods, bads


def part1(input):
    rules, lines = input.get_groups()
    befores, _ = parse_rules(rules)

    goods, _ = lines_good_and_bad(lines, befores)
    return sum([nums[len(nums)//2] for nums in goods])


e.run_tests(1, part1)
e.run_main(1, part1)


def order_correctly(nums, befores, afters):
    if len(nums) < 2:
        return nums
    pivot = nums[0]
    # These assertions are not true. Some value is first and therefore it won't appear in befores,
    # and conversely some value is last and won't be in afters
    #assert pivot in befores, f'pivot {pivot} not in befores {list(befores.keys())}'
    #assert pivot in afters, f'pivot {pivot} not in afters {list(afters.keys())}'
    left = []
    right = []
    for i in range(1, len(nums)):
        current = nums[i]
        if pivot in befores and current in befores[pivot]:
            left.append(current)
        elif pivot in afters and current in afters[pivot]:
            right.append(current)
        else:
            # Assumption failed - means that we are not given explicit ordering between every pair of numbers
            assert False, f"current {current} neither in before not after for pivot {pivot}"
    return order_correctly(left, befores, afters) + [pivot] + order_correctly(right, befores, afters)


def part2(input):
    rules, lines = input.get_groups()
    befores, afters = parse_rules(rules)

    _, bads = lines_good_and_bad(lines, befores)
    middles = 0
    for nums in bads:
        ordered = order_correctly(nums, befores, afters)
        middles += ordered[len(ordered)//2]
    return middles


e.run_tests(2, part2)
e.run_main(2, part2)
