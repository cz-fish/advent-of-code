#!/usr/bin/python3.8

import hashlib

def find_nice_hash(prefix, leading):
    i = 0
    look_for = '0' * leading
    while True:
        key = prefix + str(i)
        digest = hashlib.md5(key.encode('utf-8')).hexdigest()
        if digest.startswith(look_for):
            return i
        i += 1
        if i % 100000 == 0:
            print(f"Trying {i}")

def test(expected, prefix):
    val = find_nice_hash(prefix, 5)
    if expected == val:
        print(f"Test '{prefix}', result {val}, PASSED!")
    else:
        print(f"Test '{prefix}', result {val}, expected {expected}, FAILED!")


test(609043, "abcdef")
test(1048970, "pqrstuv")

puzzle_input = "ckczppom"
part1 = find_nice_hash(puzzle_input, 5)
print(f"Part 1: '{puzzle_input}' -> {part1}")

part2 = find_nice_hash(puzzle_input, 6)
print(f"Part 2: '{puzzle_input}' -> {part2}")
