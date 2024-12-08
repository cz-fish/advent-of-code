#!/usr/bin/python3.12

from pyaoc import Env, Grid
from collections import defaultdict

e = Env(8)
e.T("""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""", 14, 34)

e.T("""..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
..........""", 4, None)

e.T("""T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""", 3, 9)


def find_antennas(g):
    antennas = defaultdict(set)
    for row in range(g.h):
        for col in range(g.w):
            c = g.get(row, col)
            if c != '.':
                antennas[c].add((row, col))
    return antennas


def antinodes_of_kind(g, positions, antinodes):
    for i in range(len(positions)):
        first = positions[i]
        for j in range(i+1, len(positions)):
            # For each pair of positions
            second = positions[j]
            dr = second[0] - first[0]
            dc = second[1] - first[1]
            right = (second[0] + dr, second[1] + dc)
            left = (first[0] - dr, first[1] - dc)
            if g.is_in(right[0], right[1]):
                antinodes.add(right)
            if g.is_in(left[0], left[1]):
                antinodes.add(left)


def part1(input):
    g = Grid(input.get_valid_lines())
    ant = find_antennas(g)
    antinodes = set()
    for _, s in ant.items():
        antinodes_of_kind(g, list(s), antinodes)
    return len(antinodes)


e.run_tests(1, part1)
e.run_main(1, part1)


def antinodes_with_resonance(g, positions, antinodes):
    for i in range(len(positions)):
        first = positions[i]
        for j in range(i+1, len(positions)):
            # For each pair of positions
            second = positions[j]
            dr = second[0] - first[0]
            dc = second[1] - first[1]
            pos = first
            while g.is_in(pos[0], pos[1]):
                antinodes.add(pos)
                pos = (pos[0] + dr, pos[1] + dc)
            pos = (first[0] - dr, first[1] - dc)
            while g.is_in(pos[0], pos[1]):
                antinodes.add(pos)
                pos = (pos[0] - dr, pos[1] - dc)


def part2(input):
    g = Grid(input.get_valid_lines())
    ant = find_antennas(g)
    antinodes = set()
    for _, s in ant.items():
        antinodes_with_resonance(g, list(s), antinodes)
    return len(antinodes)


e.run_tests(2, part2)
e.run_main(2, part2)
