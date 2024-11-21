#!/usr/bin/python3.8

from pyaoc import Input
from collections import defaultdict, deque
import re

target = "shiny gold"

input = Input('input07.txt', ["""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""",
"""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""])

# input.use_test(1)

line_pattern = re.compile(r'^(\w+ \w+) bags contain (.*)\.$')
cont_pattern = re.compile(r'(\d+) (\w+ \w+) bags?$')

bigger_to_smaller = defaultdict(list)
smaller_to_bigger = defaultdict(list)
empties = set()

for ln in input.get_lines():
    if not ln:
        continue
    m = line_pattern.match(ln)
    # print(ln)
    assert(m is not None)
    container = m.group(1)
    contentstr = m.group(2).split(', ')
    if contentstr[0] == 'no other bags':
        empties.add(container)
    else:
        for s in contentstr:
            m = cont_pattern.match(s)
            assert(m is not None)
            count = int(m.group(1))
            containee = m.group(2)
            bigger_to_smaller[container] += [(count, containee)]
            smaller_to_bigger[containee] += [container]


def find_all_containers(start, so_far):
    for next in smaller_to_bigger[start]:
        if next in so_far:
            continue
        so_far.add(next)
        find_all_containers(next, so_far)


### Part 1
containers = set()
find_all_containers(target, containers)
print(f"Part 1: different bag colors: {len(containers)}")

### Part 2
todo = deque()
sizes = {}
for bag in empties:
    sizes[bag] = 0

todo.append(target)
while target not in sizes:
    next = todo.popleft()
    if next in sizes:
        continue
    count = 0
    all = True
    for num, bag in bigger_to_smaller[next]:
        if bag in sizes:
            count += num * (sizes[bag] + 1)
        else:
            all = False
            todo.append(bag)
    if all:
        sizes[next] = count
        # print(f"{next} -> {count}")
    else:
        todo.append(next)


print(f"Part 2: Bags in {target}: {sizes[target]}")
