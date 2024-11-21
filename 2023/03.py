#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict
from dataclasses import dataclass

e = Env(3)
e.T("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""", 4361, 467835)

@dataclass
class Number:
    val: int
    row: int
    col: int
    length: int

@dataclass
class Symbol:
    sym: str
    row: int
    col: int

def parse_input(input):
    symbols = defaultdict(list)
    numbers = defaultdict(list)
    for row, line in enumerate(input.get_valid_lines()):
        num = ''
        for col, char in enumerate(line + '.'):
            if char >= '0' and char <= '9':
                num += char
            elif num != '':
                numbers[row].append(Number(val=int(num), row=row, col=col-len(num), length=len(num)))
                num = ''
            if char != '.' and (char < '0' or char > '9'):
                symbols[row].append(Symbol(sym=char, row=row, col=col))
    return symbols, numbers


def is_next_to_symbol(number, symbols):
    left = number.col - 1
    right = number.col + number.length
    for row in range(number.row - 1, number.row + 2):
        if row not in symbols:
            continue
        for symbol in symbols[row]:
            if symbol.col >= left and symbol.col <= right:
                return True
    return False


def part1(input):
    symbols, numbers = parse_input(input)
    return sum([
        sum([
            number.val for number in line_numbers
            if is_next_to_symbol(number, symbols)
        ])
        for line_numbers in numbers.values()
    ])


e.run_tests(1, part1)
e.run_main(1, part1)


def find_neighbor_numbers(numbers, row, col):
    neighbors = []
    for row in range(row - 1, row + 2):
        if row not in numbers:
            continue
        for number in numbers[row]:
            left = number.col - 1
            right = number.col + number.length
            if col >= left and col <= right:
                neighbors.append(number)
    return neighbors


def sum_gear_ratios(numbers, symbols):
    sum_ratios = 0
    for symb_row in symbols.values():
        for symb in symb_row:
            if symb.sym != '*':
                continue
            neigbor_numbers = find_neighbor_numbers(numbers, symb.row, symb.col)
            if len(neigbor_numbers) == 2:
                sum_ratios += neigbor_numbers[0].val * neigbor_numbers[1].val
    return sum_ratios


def part2(input):
    symbols, numbers = parse_input(input)
    return sum_gear_ratios(numbers, symbols)


e.run_tests(2, part2)
e.run_main(2, part2)
