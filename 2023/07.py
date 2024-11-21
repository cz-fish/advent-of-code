#!/usr/bin/python3.8

from pyaoc import Env
from collections import Counter
from functools import cmp_to_key

e = Env(7)
e.T("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""", 6440, 5905)


def get_kind(hand):
    c = Counter(hand)
    counts = list(c.values())
    if 5 in counts:
        return 'five'
    if 4 in counts:
        return 'four'
    if 3 in counts and 2 in counts:
        return 'fullhouse'
    if 3 in counts:
        return 'three'
    if len([x for x in counts if x == 2]) == 2:
        return 'twopair'
    if 2 in counts:
        return 'pair'
    return 'highcard'


def compare_same_strength(first, second, order):
    #print(f"compare same str {first} {second}")
    assert len(first) == len(second)
    assert len(first) == 5
    for i in range(5):
        first_str = order.index(first[i])
        second_str = order.index(second[i])
        assert first_str != -1
        assert second_str != -1
        if first_str < second_str:
            #print(f"first stronger {first[i]} > {second[i]}")
            return 1
        elif second_str < first_str:
            #print(f"second stronger {first[i]} < {second[i]}")
            return -1
    assert False, f"Two hands of same strength {first} {second}"


def compare_hands(first, second):
    # Lower rank first.
    # Return -1 if first weaker than second
    # Return 1 if first stronger than second
    first_kind = get_kind(first)
    second_kind = get_kind(second)
    order = ['five', 'four', 'fullhouse', 'three', 'twopair', 'pair', 'highcard']
    f_index = order.index(first_kind)
    s_index = order.index(second_kind)
    assert f_index != -1
    assert s_index != -1
    if f_index < s_index:
        # First hand stronger
        return 1
    elif f_index > s_index:
        # Second hand stronger
        return -1
    # Both hands same strength kind
    return compare_same_strength(first, second, 'AKQJT98765432')


def part1(input):
    hands = []
    for ln in input.get_valid_lines():
        hand, bid_s = ln.split(' ')
        bid = int(bid_s)
        hands.append((hand, bid))
    # sort lowest rank to highest rank
    hands.sort(key=cmp_to_key(lambda x, y: compare_hands(x[0], y[0])))
    #print(hands)
    return sum([(i+1) * hand[1] for i, hand in enumerate(hands)])


e.run_tests(1, part1)
e.run_main(1, part1)


def get_kind_with_jokers(hand):
    jokers = len([x for x in hand if x == 'J'])
    if jokers == 0:
        return get_kind(hand)
    # There is at least one joker
    rest = Counter([x for x in hand if x != 'J'])
    counts = list(rest.values())
    if not counts:
        # All cards must have been jokers, so five of a kind
        return 'five'
    # It's never worth to use joker to make a fullhouse. It's always better to use it to make four of a kind
    # Always add jokers to the highest number
    highest = max(counts)
    for i, v in enumerate(counts):
        if v == highest:
            counts[i] += jokers
            break

    if 5 in counts:
        return 'five'
    if 4 in counts:
        return 'four'
    if 3 in counts and 2 in counts:
        return 'fullhouse'
    if 3 in counts:
        return 'three'
    if len([x for x in counts if x == 2]) == 2:
        return 'twopair'
    if 2 in counts:
        return 'pair'
    return 'highcard'


def compare_hands_with_jokers(first, second):
    # Lower rank first.
    # Return -1 if first weaker than second
    # Return 1 if first stronger than second
    first_kind = get_kind_with_jokers(first)
    second_kind = get_kind_with_jokers(second)
    order = ['five', 'four', 'fullhouse', 'three', 'twopair', 'pair', 'highcard']
    f_index = order.index(first_kind)
    s_index = order.index(second_kind)
    assert f_index != -1
    assert s_index != -1
    if f_index < s_index:
        # First hand stronger
        return 1
    elif f_index > s_index:
        # Second hand stronger
        return -1
    # Both hands same strength kind
    return compare_same_strength(first, second, 'AKQT98765432J')



def part2(input):
    hands = []
    for ln in input.get_valid_lines():
        hand, bid_s = ln.split(' ')
        bid = int(bid_s)
        hands.append((hand, bid))
    # sort lowest rank to highest rank
    hands.sort(key=cmp_to_key(lambda x, y: compare_hands_with_jokers(x[0], y[0])))
    #print(hands)
    return sum([(i+1) * hand[1] for i, hand in enumerate(hands)])


e.run_tests(2, part2)
e.run_main(2, part2)
