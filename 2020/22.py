#!/usr/bin/python3.8

from pyaoc import Env
from collections import deque

e = Env(22)
e.T("""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""", 306, 291)


def play(decks):
    rounds = 0
    while True:
        if not decks[0] or not decks[1]:
            return rounds
        draw = [decks[0].popleft(), decks[1].popleft()]
        if draw[0] > draw[1]:
            decks[0].append(draw[0])
            decks[0].append(draw[1])
        else:
            decks[1].append(draw[1])
            decks[1].append(draw[0])
        rounds += 1


def sum_decks(decks):
    results = []
    for deck in decks:
        counter = 1
        result = 0
        while deck:
            val = deck.pop()
            result += val * counter
            counter += 1
        results.append(result)
    return results


def part1(input):
    gr = input.get_groups()
    assert len(gr) == 2
    decks = [deque([int(i) for i in gr[0][1:]]), deque([int(i) for i in gr[1][1:]])]
    rounds = play(decks)
    results = sum_decks(decks)
    print(f"{rounds} rounds: scores {results}")
    return max(results)


e.run_tests(1, part1)
e.run_main(1, part1)


def deck_id(decks):
    d = list(decks[0]) + [0] + list(decks[1])
    q = 51
    id = 0
    for v in d:
        id += v * q
        q *= 51
    return id


def deck_id2(decks):
    d = tuple(list(decks[0]) + [0] + list(decks[1]))
    return hash(d)


def play_part2(decks):
    rounds = 0
    known_states = set()
    while True:
        if not decks[0] or not decks[1]:
            return rounds

        # decks configuration -> large int - cca 9 seconds to complete the problem
        # state = deck_id(decks)

        # decks configuration -> string - cca 10 seconds to complete the problem
        # state = ','.join([str(x) for x in list(decks[0])]) + ':' + ','.join([str(x) for x in list(decks[1])])

        # decks configuration -> hash (small int) - cca 2 seconds. Potentially wrong, but for the given input, the result looks correct.
        state = deck_id2(decks)

        if state in known_states:
            # cycle detected. Player 1 wins
            decks[1].clear()
            return rounds
        known_states.add(state)

        rounds += 1

        draw = [decks[0].popleft(), decks[1].popleft()]
        if len(decks[0]) >= draw[0] and len(decks[1]) >= draw[1]:
            # enough cards to recurse
            rdecks = [deque(list(decks[0])[:draw[0]]), deque(list(decks[1])[:draw[1]])]
            play_part2(rdecks)
            if not rdecks[0]:
                round_winner = 1
            else:
                round_winner = 0
            # print(f"round {rounds} recursive game winner {round_winner}")
        else:
            if draw[0] > draw[1]:
                round_winner = 0
            else:
                round_winner = 1

        decks[round_winner].append(draw[round_winner])
        decks[round_winner].append(draw[-round_winner + 1])


def part2(input):
    gr = input.get_groups()
    assert len(gr) == 2
    decks = [deque([int(i) for i in gr[0][1:]]), deque([int(i) for i in gr[1][1:]])]
    rounds = play_part2(decks)
    results = sum_decks(decks)
    print(f"{rounds} rounds: scores {results}")
    return max(results)


e.run_tests(2, part2)
e.run_main(2, part2)
