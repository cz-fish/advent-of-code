#!/usr/bin/python3.8

from aoc import Env

e = Env(11)
e.T("18", "33,45", "90,269,16")
e.T("42", "21,61", "232,251,12")


def get_cell_power(x, y, serial_num):
    rack_id = x + 10
    power_level = (rack_id * y + serial_num) * rack_id
    power_digit = (power_level % 1000) // 100
    return power_digit - 5


def get_all_cell_powers(serial_num):
    all_powers = []
    for y in range(1, 301):
        all_powers.append([])
        for x in range(1, 301):
            all_powers[-1].append(get_cell_power(x, y, serial_num))
    return all_powers


def find_best_of_size(all_powers, size):
    hei = len(all_powers)
    wid = len(all_powers[0])
    best = None
    best_coord = None
    columns = [
        sum(all_powers[y][x] for y in range(size))
        for x in range(wid)
    ]
    for y in range(hei - size + 1):
        value = sum(columns[0:size])
        for x in range(0, wid - size + 1):
            if best is None or value > best:
                best = value
                best_coord = f"{x+1},{y+1}"
            if x < wid - size:
                value = value - columns[x] + columns[x+size]
        if y < hei - size:
            for x in range(wid):
                columns[x] = columns[x] - all_powers[y][x] + all_powers[y+size][x]
    return best_coord, best


def part1(input):
    serial_num = input.get_all_ints()[0]
    all_powers = get_all_cell_powers(serial_num)
    best_coord, best = find_best_of_size(all_powers, 3)
    print(f"best total power {best}")
    return best_coord


# Test get_cell_power
assert(get_cell_power(3, 5, 8) == 4)
assert(get_cell_power(122, 79, 57) == -5)
assert(get_cell_power(217, 196, 39) == 0)
assert(get_cell_power(101, 153, 71) == 4)

e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    serial_num = input.get_all_ints()[0]
    all_powers = get_all_cell_powers(serial_num)
    uberbest = None
    uberbest_coord = None
    for size in range(1, 301):
        best_coord, best = find_best_of_size(all_powers, size)
        if uberbest is None or best > uberbest:
            uberbest = best
            uberbest_coord = f"{best_coord},{size}"
    print(f"best total power {uberbest}")
    return uberbest_coord


e.run_tests(2, part2)
e.run_main(2, part2)
