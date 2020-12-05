#!/usr/bin/python3.8

from collections import defaultdict

with open('input05.txt', 'rt') as f:
    bpasses = [ln.strip() for ln in f.readlines()]


def parse_bpass(bp):
    row = int(''.join([{'F':'0','B':'1'}[i] for i in bp[:7]]), 2)
    col = int(''.join([{'L':'0','R':'1'}[i] for i in bp[7:]]), 2)
    return row, col, row * 8 + col


assert(parse_bpass("FBFBBFFRLR") == (44, 5, 357))
assert(parse_bpass("BFFFBBFRRR") == (70, 7, 567))
assert(parse_bpass("FFFBBBFRRR") == (14, 7, 119))
assert(parse_bpass("BBFFBBFRLL") == (102, 4, 820))

seats = [parse_bpass(x) for x in bpasses]
seat_ids = [x[2] for x in seats]
max_id = max(seat_ids)

print(f"Part 1: {max_id}")


occu = defaultdict(set)
seat_set = set(seat_ids)

for row, col, id in seats:
    occu[row].add(col)

for row, x in occu.items():
    if len(x) == 7:
        col = [i for i in range(8) if i not in x][0]
        id = row * 8 + col
        if (id - 1) in seat_set and (id + 1) in seat_set:
            print(f"Part 2: seat {row}, {col} -> id {id}")
