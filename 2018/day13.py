#!/usr/bin/env python3

import sys

with open('day13.txt', 'rt') as f:
    graph = [[c for c in l] for l in f.readlines()]

h = len(graph)
w = len(graph[0])

TURNS = 'LSR'
# L S R / \
DIRS = {
    '<': ((-1,0), 'v<^v^'),
    '^': ((0,-1), '<^>><'),
    '>': ((1,0), '^>v^v'),
    'v': ((0,1), '>v<<>')
}

class Trolley:
    def __init__(self, x, y, dire):
        self.x = x
        self.y = y
        self.dire = dire
        self.nextturn = 'L'
    
    def move(self, graph):
        move = DIRS[self.dire]
        self.x += move[0][0]
        self.y += move[0][1]
        c = graph[self.y][self.x]
        if c == '+':
            t = TURNS.find(self.nextturn)
            self.dire = move[1][t]
            self.nextturn = TURNS[(t + 1)%3]
        elif c == '/':
            self.dire = move[1][3]
        elif c == '\\':
            self.dire = move[1][4]
    
    def __str__(self):
        return "[{},{} {} {}]".format(self.x, self.y, self.dire, self.nextturn)

def crashed(idx, trolleys):
    T = trolleys[idx]
    for i, t in enumerate(trolleys):
        if i == idx: continue
        if t.x == T.x and t.y == T.y:
            return True
    return False

trolleys = []

for row, r in enumerate(graph):
    for col, c in enumerate(r):
        if c in '<^>v':
            trolleys += [Trolley(col, row, c)]
            if c in '<>': r[col] = '-'
            else: r[col] = '|'

#print(trolleys)
print(h, w, len(trolleys))

cnt = 0
while True:
    print(cnt, ', '.join([str(t) for t in trolleys]))
    cnt+=1

    for i, t in enumerate(trolleys):
        t.move(graph)

        if crashed(i, trolleys):
            print(t.x, t.y)
            sys.exit(0)
    
    trolleys.sort(key=lambda t: (t.y, t.x))