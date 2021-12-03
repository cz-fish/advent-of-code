#!/usr/bin/env python3

import sys

players = int(sys.argv[1])
marbles = int(sys.argv[2])

ll = [0]
scores = [0] * players
max_score = None
player = 0
current = 0

for i in range(1, marbles+1):
    if i % 23 == 0:
        pos = (current - 7) % len(ll)
        rem = (current - 6) % len(ll)
        scores[player] += i + ll[rem]
        if max_score is None or scores[player] > max_score:
            max_score = scores[player]
        ll = ll[:rem] + ll[rem+1:]
        current = pos
    else:
        pos = (current + 2) % len(ll)
        ll = ll[:pos+1] + [i] + ll[pos+1:]
        current = pos

    #print (ll)
    
    player = (player + 1) % players

print(max_score)