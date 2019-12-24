#!/usr/bin/python3.8

grid = []

with open('input24.txt', 'rt') as f:
    for ln in f.readlines():
        grid += [ln.strip()]

#time = 10
#time = 2
time = 200

halftime = time // 2

grids = []
for t in range(time + 1):
    if t == halftime:
        grids += [grid]
    else:
        grids += [
            ['.....'] * 5
        ]

def bugcount():
    count = 0
    for layer in grids:
        count += sum([ln.count('#') for ln in layer])
    return count

def next_minute_layer(grid, grid_p1, grid_m1):
    # top, right, bottom, left from the outer and inner grids
    outer = [1 if x == '#' else 0 for x in [grid_m1[1][2], grid_m1[2][3], grid_m1[3][2], grid_m1[2][1]]]
    inner = [
        grid_p1[0].count('#'),
        sum([1 for x in range(5) if grid_p1[x][4] == '#']),
        grid_p1[4].count('#'),
        sum([1 for x in range(5) if grid_p1[x][0] == '#'])
    ]

    ngrid = []
    for y in range(5):
        ngrid += ['']
        for x in range(5):
            if x == 2 and y == 2:
                c = '?'
            else:
                nei = ''
                if x > 0:
                    nei += grid[y][x-1]
                if x < 4:
                    nei += grid[y][x+1]
                if y > 0:
                    nei += grid[y-1][x]
                if y < 4:
                    nei += grid[y+1][x]

                bugs = nei.count('#')

                if x == 0:
                    bugs += outer[3]
                elif x == 4:
                    bugs += outer[1]
                if x == 2:
                    if y == 1:
                        bugs += inner[0]
                    elif y == 3:
                        bugs += inner[2]

                if y == 0:
                    bugs += outer[0]
                elif y == 4:
                    bugs += outer[2]
                elif y == 2:
                    if x == 1:
                        bugs += inner[3]
                    elif x == 3:
                        bugs += inner[1]

                c = grid[y][x]
                if c == '#' and bugs != 1:
                    c = '.'
                elif c == '.' and (bugs == 1 or bugs == 2):
                    c = '#'
            ngrid[-1] += c
    return ngrid


def next_minute(time):
    global grids
    pending = {}
    dist = time // 2 + 1
    empty = ['.....'] * 5

    for t in range(dist + 1):
        this1 = grids[halftime - t]
        if t == dist:
            prev1 = empty
        else:
            prev1 = grids[halftime - t - 1]
        next1 = grids[halftime - t + 1]
        gen1 = next_minute_layer(this1, next1, prev1)
        pending[halftime - t] = gen1
        if t > 0:
            this2 = grids[halftime + t]
            prev2 = grids[halftime + t - 1]
            if t == dist:
                next2 = empty
            else:
                next2 = grids[halftime + t + 1]
            gen2 = next_minute_layer(this2, next2, prev2)
            pending[halftime + t] = gen2

    for t in range(dist + 1):
        grids[halftime - t] = pending[halftime - t]
        if t > 0:
            grids[halftime + t] = pending[halftime + t]


def print_em_all():
    for layer in range(time + 1):
        print(f'layer {layer - halftime}')
        for ln in grids[layer]:
            print(ln)
        print('----------')
    print('====================')

#print('time 0')
#print_em_all()

for t in range(time):
    next_minute(t)
    #print(f'time {t+1}')
    #print_em_all()


#print_em_all()

print(f'After {time} minutes: {bugcount()} bugs')
