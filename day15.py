#!/usr/bin/env python3

import queue
import sys

class Actor:
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y
        self.hp = 200
        self.ap = 3

    def __repr__(self):
        return '[{} ({}, {}) {}]'.format(self.char, self.x, self.y, self.hp)

grid = []
actors = []
elves = set()
goblins = set()

def printState():
    for l in grid:
        print(''.join(l))
    for a in actors:
        print(a)
    print('------------------')

suffix = ''
if len(sys.argv) > 1:
    suffix = sys.argv[1]
source = 'inputs/day15{}.txt'.format(suffix)
with open(source, 'rt') as f:
    for y, l in enumerate(f.readlines()):
        grid += [[]]
        for x, c in enumerate(l.strip()):
            if c in 'EG':
                a = Actor(c, x, y)
                actors += [a]
                if c == 'E':
                    elves.add(a)
                else:
                    goblins.add(a)
            grid[-1] += [c]

def moveTurn(actor):
    #print(actor)
    x = actor.x
    y = actor.y
    other = 'EG'[actor.char == 'E']
    if grid[y][x-1] == other or grid[y][x+1] == other or grid[y-1][x] == other or grid[y+1][x] == other:
        # Already next to an enemy - no move
        return x,y
    
    q = queue.Queue()
    inrange = []
    seen = set()
    q.put((x, y, []))
    while not q.empty():
        nx, ny, p = q.get()
        if inrange and len(inrange[0][2]) < len(p):
            # Already found targets that are closer than this
            break
        for ox, oy in [(nx, ny-1), (nx-1,ny), (nx+1,ny), (nx,ny+1)]:
            h = '{},{}'.format(ox,oy)
            if h in seen:
                continue
            seen.add(h)
            if grid[oy][ox] == other:
                inrange += [(nx, ny, p + [(nx, ny)])]
            elif grid[oy][ox] == '.':
                q.put((ox, oy, p + [(nx, ny)]))

    if not inrange:
        # Cannot move
        return x,y
    
    inrange.sort(key=lambda r: (len(r[2]), r[1], r[0]))
    #print(inrange)

    target = inrange[0]
    path = target[2]
    return path[1]


def fight(actor):
    x = actor.x
    y = actor.y
    other = 'EG'[actor.char == 'E']
    opo = []
    if other == 'E':
        oact = elves
    else:
        oact = goblins
    for ox, oy in [(x,y-1), (x-1,y), (x+1,y), (x,y+1)]:
        if grid[oy][ox] == other:
            for o in oact:
                if o.x == ox and o.y == oy:
                    opo += [o]
                    break
            else:
                raise Exception("oponent of class {} not found at {}, {}".format(other, ox, oy))

    if not opo:
        # No-one to fight
        return None, None
    
    opo.sort(key=lambda a:(a.hp, a.y, a.x))
    return opo[0], oact


turn = 0
while True:
    #print("-- after {} rounds ---".format(turn))
    #printState()
    if not elves or not goblins:
        print("-- after {} rounds ---".format(turn))
        printState()
        break
    #if turn >= 2:
    #    break
    killed = set()
    for a in actors:
        if a in killed:
            continue
        
        if not elves or not goblins:
            break

        move = moveTurn(a)
        grid[a.y][a.x] = '.'
        a.x = move[0]
        a.y = move[1]
        grid[a.y][a.x] = a.char

        opo, group = fight(a)
        if opo:
            opo.hp -= a.ap
            if opo.hp <= 0:
                killed.add(opo)
                group.remove(opo)
                grid[opo.y][opo.x] = '.'
    else:
        turn += 1

    for a in killed:
        actors.remove(a)
    actors.sort(key=lambda a: (a.y, a.x))


score = sum([g.hp for g in goblins]) + sum([e.hp for e in elves])
score = score * turn
print("score", score)
