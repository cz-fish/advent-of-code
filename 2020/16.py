#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict
import re

e = Env(16)
e.T("""departure class: 1-3 or 5-7
departure row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""", 71, 1*7)
e.T("""departure class: 0-1 or 4-19
departure row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""", None, 12*11)


def parse_input(input):
    gr = input.get_groups()
    fields = {}
    for ln in gr[0]:
        m = re.match(r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)', ln)
        assert m is not None
        field = m.group(1)
        M = [int(m.group(x)) for x in [2,3,4,5]]
        fields[field] = M

    yourT = [int(x) for x in gr[1][1].split(',')]

    otherT = []
    for ln in gr[2][1:]:
        t = [int(x) for x in ln.split(',')]
        otherT += [t]

    assert(len(fields) == len(yourT))
    assert(len(fields) == len(otherT[0]))
    return fields, yourT, otherT


def get_all_filters(fields):
    all_filters = []
    for f in fields.values():
        all_filters.append((f[0], f[1]))
        all_filters.append((f[2], f[3]))
    return all_filters


def part1(input):
    fields, _, otherT = parse_input(input)
    all_filters = get_all_filters(fields)

    error_rate = 0
    for ticket in otherT:
        for field in ticket:
            check = lambda filter: field >= filter[0] and field <= filter[1]
            m = any([check(filter) for filter in all_filters])
            if not m:
                error_rate += field

    return error_rate


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    fields, yourT, otherT = parse_input(input)
    all_filters = get_all_filters(fields)
    # filter out bad tickets - only keep good ones
    goodT = []
    for ticket in otherT:
        for field in ticket:
            check = lambda filter: field >= filter[0] and field <= filter[1]
            m = any([check(filter) for filter in all_filters])
            if not m:
                break
        else:
            goodT += [ticket]

    # filter out which colums can be which, based on just the values from the tickets
    canBe = {}
    all_cols = [i for i in range(len(yourT))]
    for field in fields.keys():
        canBe[field] = set(all_cols)

    for ticket in goodT:
        for column, value in enumerate(ticket):
            for field, rng in fields.items():
                if (value < rng[0] or value > rng[1]) and (value < rng[2] or value > rng[3]):
                    # print(f"{field} cannot be column {column} because value {value} not in {rng}")
                    canBe[field] = canBe[field] - {column}

    # now some columns can still be multiple fields, but hopefully some columns will already be
    # determined. And then we keep removing those fixed columns from canBe, until we determine
    # everything
    print("Filtered columns")
    for field, opts in canBe.items():
        print(f"  {field} can be {opts}")

    fixedColumns = set()
    change = True
    while change:
        change = False
        newFixedColumns = {}
        for field, opts in canBe.items():
            assert(len(opts)), f"There are no more options for field {field}!"
            if len(opts) == 1:
                column = list(opts)[0]
                assert(column not in newFixedColumns), f"column {column} is the only possible for multiple fields!"
                newFixedColumns[column] = field
        removeColumns = set(newFixedColumns.keys()) - fixedColumns
        for column in removeColumns:
            for field, opts in canBe.items():
                if newFixedColumns[column] != field and column in opts:
                    opts.remove(column)
        fixedColumns = fixedColumns.union(removeColumns)
        change = bool(removeColumns)

    assert len(fixedColumns) == len(yourT), f"some fields were not mapped! {canBe}"

    print("Assigned columns")

    result = 1
    for field, columns in canBe.items():
        column = list(columns)[0]
        print(f"  {field} is {column}")
        if field.startswith("departure "):
            result *= yourT[column]

    return result


e.run_tests(2, part2)
e.run_main(2, part2)
