#!/usr/bin/env python3

import re
import queue

cloud = []

r = re.compile(r'^([xy])=(\d+), .=(\d+)\.\.(\d+)')

with open('inputs/day17.txt', 'rt') as f:
    for ll in f.readlines():
        m = r.match(ll)
        if not m:
            raise Exception("Line doesn't match: " + ll)
        d = m.group(1)
        a = int(m.group(2))
        b = int(m.group(3))
        c = int(m.group(4))

        for i in range(b, c+1):
            if d == 'x':
                cloud += [(a, i)]
            else:
                cloud += [(i, a)]

class State:
    def __init__(self, cloud):
        cloud.sort(key=lambda a:a[0])
        self.minx = cloud[0][0] - 1
        self.maxx = cloud[-1][0] + 1
        cloud.sort(key=lambda a:a[1])
        self.miny = cloud[0][1]
        self.maxy = cloud[-1][1]

        c = {}
        for x, y in cloud:
            if y not in c:
                c[y] = set()
            c[y].add(x)

        self.grid = []
        for y in range(self.maxy+1):
            self.grid += [[]]
            if y in c:
                xes = c[y]
            else:
                xes = set()
            for x in range(self.maxx+1):
                self.grid[-1] += ['.', '#'][x in xes]
        self.grid[0][500] = '+'

    def xpm(self):
        lx = self.maxx+1
        ly = self.maxy+1
        print('''! XPM2
{} {} 5 1
. c #ffcc00
# c #663300
~ c #0066ff
| c #669900
+ c #ff3300'''.format(lx - self.minx, ly - 0))
        for y in range(0, ly):
            l = self.grid[y]
            print(''.join(l[self.minx:lx]))
    
    def count(self, dry):
        c = 0
        if dry:
            valid = '~'
        else:
            valid = '|~'
        for y in range(self.miny, self.maxy+1):
            for x in range(self.minx, self.maxx+1):
                if self.grid[y][x] in valid:
                    c += 1
        return c
    
    def find_pot(self, start):
        x, y = start
        while y < self.maxy:
            c = self.grid[y+1][x]
            if c == '#' or c == '~':
                return (x, y)
            elif c == '|':
                return None
            self.grid[y+1][x] = '|'
            y += 1
        return None
    
    def fill_pot(self, start):
        x, y = start
        while True:
            overflow = self.fill_line((x, y))
            if not overflow:
                y -= 1
                if y == 0:
                    return []
            else:
                return overflow

    def _find_border(self, x, y, cond, step):
        border = x
        i = x + step
        while cond(i):
            if self.grid[y][i] not in '.|':
                return border, None
            border = i
            below = self.grid[y+1][i]
            if below == '.' or below == '|':
                return border, (i, y)
            i += step
        return border, None

    def fill_line(self, start):
        x, y = start

        left, o1 = self._find_border(x, y, lambda i: i >= 0, -1)
        right, o2 = self._find_border(x, y, lambda i: i <= self.maxx, 1)
        overflow = [o for o in [o1, o2] if o]

        if not overflow:
            c = '~'
        else:
            c = '|'
        
        for i in range(left, right+1):
            self.grid[y][i] = c

        return overflow


state = State(cloud)

sources = queue.Queue()
sources.put((500,0))

while not sources.empty():
    s = sources.get()
    pot = state.find_pot(s)
    if not pot:
        continue
    more_sources = state.fill_pot(pot)
    for s in more_sources:
        sources.put(s)

#state.xpm()
print(state.count(False))
print(state.count(True))

