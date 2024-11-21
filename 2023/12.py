#!/usr/bin/python3.8

from pyaoc import Env

e = Env(12)

e.T("???.### 1,1,3", 1, 1)
e.T(".??..??...?##. 1,1,3", 4, 16384)
e.T("?#?#?#?#?#?#?#? 1,3,1,6", 1, 1)
e.T("????.#...#... 4,1,1", 1, 16)
e.T("????.######..#####. 1,6,5", 4, 2500)
e.T("?###???????? 3,2,1", 10, 506250)

e.T("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""", 21, 525152)

e.T("?????? 1", 6, None)
e.T("???? 1,1", 3, None)
e.T("?????.????.# 4,1,1", 8, None)

def count_possibilities_very_slowly(pattern, numbers):
    def pattern_match(s, numbers):
        groups = []
        group = 0
        s = s + '.'
        for c in s:
            if c == '#':
                group += 1
            elif c == '.':
                if group > 0:
                    groups.append(group)
                group = 0
        return groups == numbers

    def add_char(s):
        size = len(s)
        if size == len(pattern):
            return 1 if pattern_match(s, numbers) else 0
        c = pattern[size]
        if c in '.#':
            return add_char(s + c)
        elif c == '?':
            count = add_char(s + '.')
            return count + add_char(s + '#')
        else:
            assert False, f"Wrong pattern character '{c}'"

    return add_char('')


def can_fit(pattern, start, block_length):
    # If any of the positions where we want to place the block is '.', we
    # can't place the block
    for i in range(block_length):
        if pattern[start + i] == '.':
            return False
    # If we placed the block but the next position afterwards is another block
    # position, not a space, then we can't place the block
    if start + block_length < len(pattern):
        if pattern[start + block_length] == '#':
            return False
    return True

def rest_all_empty(pattern, start):
    for i in range(start, len(pattern)):
        if pattern[i] == '#':
            return False
    return True

def place_next_block(pattern, numbers, pattern_offset, number_offset, wiggle, memo):
    count = 0
    next_num = numbers[number_offset]
    new_number_offset = number_offset + 1
    for wiggle_used in range(wiggle + 1):
        start = pattern_offset + wiggle_used
        if can_fit(pattern, start, next_num):
            # we place block of size `next_num` at position `start`
            # what remains?
            if new_number_offset < len(numbers):
                # there are more blocks to be placed
                new_pattern_offset = pattern_offset + next_num + 1 + wiggle_used
                new_wiggle = wiggle - wiggle_used
                if (new_pattern_offset, new_number_offset, new_wiggle) in memo:
                    count += memo[(new_pattern_offset, new_number_offset, new_wiggle)]
                else:
                    count += place_next_block(
                        pattern,
                        numbers,
                        new_pattern_offset,
                        new_number_offset,
                        new_wiggle,
                        memo)
            else:
                # this was the last block
                # The rest of pattern has to be all empty, otherwise this is not a fit
                count += 1 if rest_all_empty(pattern, pattern_offset + next_num + wiggle_used) else 0
        if pattern[pattern_offset + wiggle_used] == '#':
            # cannot skip any more, as that would skip over a # position
            break
    memo[(pattern_offset, number_offset, wiggle)] = count
    return count

def count_possibilities(pattern, numbers):
    min_size = sum(numbers) + len(numbers) - 1
    wiggle = len(pattern) - min_size
    assert wiggle >= 0, f"Not enough space in pattern '{pattern}' (len {len(pattern)}) for {numbers} (len {min_size})"
    pattern_offset = 0
    number_offset = 0
    memo = {}
    options = place_next_block(pattern, numbers, pattern_offset, number_offset, wiggle, memo)
    return options


def part1(input):
    total = 0
    for ln in input.get_valid_lines():
        pattern, nums = ln.split()
        numbers = [int(x) for x in nums.split(',')]
        #count0 = count_possibilities_very_slowly(pattern, numbers)
        count = count_possibilities(pattern, numbers)
        #if count != count0:
        #    print(f"Mismatch: {ln} got {count0} and {count}")
        total += count
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    total = 0
    for ln in input.get_valid_lines():
        pattern, nums = ln.split()
        numbers = [int(x) for x in nums.split(',')]
        pattern = '?'.join([pattern for _ in range(5)])
        numbers = numbers * 5
        #print(pattern, numbers)
        total += count_possibilities(pattern, numbers)
    return total


e.run_tests(2, part2)
e.run_main(2, part2)
