#!/usr/bin/python3.8

from aoc import Env

e = Env(20)
e.T("""1
2
-3
3
-2
0
4""", 3, 1623178306)

VAL = 0
PREV = 1
NEXT = 2


# Linked list kind of solution. Actually move each number N places
# in the list. Slow, but fast enough for part 1
def mix(numbers):
    mixed = []
    for i, num in enumerate(numbers):
        if i == 0:
            prev = len(numbers) - 1
        else:
            prev = i - 1
        next = (i + 1) % len(numbers)
        mixed.append([num, prev, next])
    
    for i in range(len(mixed)):
        val = mixed[i][VAL]
        for j in range(abs(val)):
            p = mixed[i][PREV]
            n = mixed[i][NEXT]
            if val < 0:
                # swap i and prev
                prev_prev = mixed[p][PREV]
                mixed[p][PREV] = i
                mixed[prev_prev][NEXT] = i
                mixed[i][PREV] = prev_prev

                mixed[p][NEXT] = n
                mixed[i][NEXT] = p
                mixed[n][PREV] = p
            else:
                # swap i and next
                next_next = mixed[n][NEXT]
                mixed[n][NEXT] = i
                mixed[next_next][PREV] = i
                mixed[i][NEXT] = next_next

                mixed[n][PREV] = p
                mixed[i][PREV] = n
                mixed[p][NEXT] = n
    
    return mixed


# 'mixed' parameter is a "linked list" - list of 3 integers (value, prev, next).
# the function copies the values into a list of numbers in the right order, starting
# with the value 0
def extract(mixed):
    zero_index = None
    for i, v in enumerate(mixed):
        if v[0] == 0:
            zero_index = i
            break
    assert zero_index is not None
    in_order = [mixed[zero_index][VAL]]
    index = mixed[zero_index][NEXT]
    while index != zero_index:
        in_order.append(mixed[index][VAL])
        index = mixed[index][NEXT]
    return in_order


"""
# This didn't work
def mix_big(numbers):
    l = len(numbers)
    order = [i for i in range(l)]
    #print(numbers, order)
    for i in range(l):
        index = order[i]
        val = numbers[index]
        #print(f"moves {val}")
        if val == 0:
            continue
        new_pos = (index + val) % l
        if val > 0:
            new_pos = (new_pos + 1) % l
        old_pos = index

        # |a b c(O) e f g(N) h i j|
        # |a b <- e f g  [c] h i j|
        #
        # |a b c(N) e f g(O) h i j|
        # |a b c [g]-> e f | h i j|
        #
        # the part between New(N) and Old(O)
        # moves either left if O < N or right if N < O

        if old_pos < new_pos:
            numbers = numbers[:old_pos] + numbers[old_pos+1:new_pos] + [val] + numbers[new_pos:]
            left = old_pos
            right = new_pos
            diff = -1
        else:
            numbers = numbers[:new_pos] + [val] + numbers[new_pos:old_pos] + numbers[old_pos+1:]
            left = new_pos + 1
            right = old_pos + 1
            diff = 1
        
        for j in range(i+1, l):
            if order[j] >= left and order[j] < right:
                order[j] += diff
        #print(numbers, order)
    return numbers
"""

"""
# This didn't work
def mix_big_in_order_0(numbers, order):
    l = len(numbers)
    for val in (order):
        index = numbers.index(val)
        if val == 0:
            continue
        # going over the original position again more_steps times
        if val > 0:
            more_steps = val // l
        else:
            more_steps = (val + 1) // l

        new_pos = (index + val + more_steps) % l
        old_pos = index
        if val > 0:
            new_pos = (new_pos + 1) % l
        #print(f"{val} moves from {old_pos} to before {new_pos}")

        # |a b c(O) e f g(N) h i j|
        # |a b <- e f g  [c] h i j|
        #
        # |a b c(N) e f g(O) h i j|
        # |a b c [g]-> e f | h i j|
        #
        # the part between New(N) and Old(O)
        # moves either left if O < N or right if N < O

        if old_pos < new_pos:
            numbers = numbers[:old_pos] + numbers[old_pos+1:new_pos] + [val] + numbers[new_pos:]
        else:
            numbers = numbers[:new_pos] + [val] + numbers[new_pos:old_pos] + numbers[old_pos+1:]
        
        #print(numbers)
    return numbers
"""

# Every number is a tuple - the value and its original position.
# There can be multiple same numbers in the input list, and we use
# the original position / index to find the right element to move
def mix_big_in_order(numbers):
    l = len(numbers)

    def find_index(numbers, order):
        for i, n in enumerate(numbers):
            if order == n[1]:
                return i
        assert False

    # Go in the order of numbers in the original list
    for order in range(l):
        index = find_index(numbers, order)
        val = numbers[index][0]
        if val == 0:
            continue
        # take the value out
        numbers = numbers[:index] + numbers[index + 1:]
        # find new position
        if index == l - 1:
            newpos = val % (l - 1)
        else:
            newpos = (index + val) % (l - 1)
        # put number back
        numbers = numbers[:newpos] + [(val, order)] + numbers[newpos:]
    return numbers


# Take a list of tuples (value, original position), and produce a list
# of just the numbers, in the right order, starting with the 0 value
def rotate_to_zero(numbers):
    numbers = [k for k, v in numbers]
    zero_index = numbers.index(0)
    return numbers[zero_index:] + numbers[:zero_index]


# This uses the slower linked-list approach
def part1_(input):
    numbers = input.get_ints()
    mixed = mix(numbers)
    in_order = extract(mixed)
    l = len(in_order)
    return in_order[1000 % l] + in_order[2000 % l] + in_order[3000 % l]

# This uses the faster modular index approach
def part1(input):
    numbers = input.get_ints()
    numbers = [(n, i) for i, n in enumerate(numbers)]
    mixed = mix_big_in_order(numbers)
    in_order = rotate_to_zero(mixed)
    l = len(in_order)
    return in_order[1000 % l] + in_order[2000 % l] + in_order[3000 % l]

e.run_tests(1, part1)
e.run_main(1, part1)
#e.run_main(1, part1_)


def part2(input):
    key = 811589153
    repeats = 10

    numbers = input.get_ints()
    numbers = [(n * key, i) for i, n in enumerate(numbers)]
    for _ in range(repeats):
        numbers = mix_big_in_order(numbers)
    in_order = rotate_to_zero(numbers)
    l = len(in_order)
    return in_order[1000 % l] + in_order[2000 % l] + in_order[3000 % l]


e.run_tests(2, part2)
e.run_main(2, part2)
