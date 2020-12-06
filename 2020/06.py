#!/usr/bin/python3.8

groups = [[]]
with open('input06.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        if not ln:
            groups += [[]]
        else:
            groups[-1] += [ln]


def count_group(group):
    return len(set(''.join(group)))


def recount_group(group):
    a = None
    for ans in group:
        if a is None:
            a = set(ans)
        else:
            a = a.intersection(set(ans))
    return len(a)


total = sum([count_group(gr) for gr in groups])
print(f"Part 1: sum {total}")

recounted = sum([recount_group(gr) for gr in groups])
print(f"Part 2: sum {recounted}")
