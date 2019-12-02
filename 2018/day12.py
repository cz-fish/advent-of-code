#!/usr/bin/env python3

state = []
rules = {}
iter = 20

with open('day12.txt', 'rt') as f:
    state = f.readline().strip()[15:]
    f.readline()
    l = f.readline()
    while len(l) > 2:
        rules[l[:5]] = l[9]
        l = f.readline()

ll = len(state)
offset = iter * 2 + 2
w = '.' * offset + state + '.' * offset

print('   {}0{}{}'.format(' ' * offset, ' ' * (ll-2), ll))
print(' 0 {}'.format(w))

for i in range(iter):
    n = ['.'] * (ll + 2*offset)
    for j in range(offset - i*2, offset + ll + i*2 + 1):
        p = w[j-2:j+3]
        if p in rules:
            n[j] = rules[p]
    w = ''.join(n)
    print('{:2} {}'.format(i+1, w))

score = sum([i - offset for i in range(len(w)) if w[i] == '#'])
print(score)