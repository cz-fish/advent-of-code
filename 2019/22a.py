#!/usr/bin/python3.8

deck_size = 10007
#deck_size = 10

deck = list(range(deck_size))


def with_increment(deck, n):
    l = len(deck)
    out = [0] * l
    i = 0
    for j in range(l):
        out[i] = deck[j]
        i = (i + n) % l
    return out


with open('input22.txt', 'rt') as f:
    for line in f.readlines():
        if line.startswith('deal with increment '):
            n = int(line[len('deal with increment '):])
            deck = with_increment(deck, n)
        elif line.startswith('deal into new stack'):
            deck = deck[::-1]
        elif line.startswith('cut '):
            n = int(line[len('cut '):])
            deck = deck[n:] + deck[:n]
        else:
            print('Unknown line: "' + line.strip() + '"')


if deck_size > 2019:
    print("Position of 2019 card:", deck.index(2019))
else:
    print(deck)
