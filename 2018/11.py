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


def find_best_of_size_slowest(all_powers, size):
    best = None
    best_coord = None
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            value = 0
            for z in range(size):
                value += sum(all_powers[y-1+z][x-1:x-1+size])
            if best is None or value > best:
                best = value
                best_coord = f"{x},{y}"
    return best_coord, best


def count_square(all_powers, size, x, y):
    value = 0
    for z in range(size):
        value += sum(all_powers[y-1+z][x-1:x-1+size])
    return value


def column(all_powers, x, ymin, ymax):
    return sum(
        all_powers[y][x-1]
        for y in range(ymin-1, ymax-1)
    )


def find_best_of_size(all_powers, size):
    best = count_square(all_powers, size, 1, 1)
    best_coord = "1,1"
    for y in range(1, 302 - size):
        value = count_square(all_powers, size, 1, y)
        if value > best:
            best = value
            best_coord = f"1,{y}"
        for x in range(2, 302 - size):
            value = value + column(all_powers, x+size-1, y, y+size) - column(all_powers, x-1, y, y+size)
            if value > best:
                best = value
                best_coord = f"{x},{y}"
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
