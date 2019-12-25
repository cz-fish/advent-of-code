#!/usr/bin/python3.8

# deck_size = 10007
# deck_size = 10
deck_size = 119315717514047


def with_increment(n, pos):
    mult_inv = pow(n, -1, deck_size)
    return (pos * mult_inv) % deck_size

def reverse(pos):
    return deck_size - 1 - pos

def cut(n, pos):
    rem = deck_size - n
    if pos < rem:
        return pos + n
    else:
        return pos - rem

instr = []
itext = []
with open('input22.txt', 'rt') as f:
    for line in f.readlines():
        if line.startswith('deal with increment '):
            n = int(line[len('deal with increment '):])
            instr += [lambda pos, n=n: with_increment(n, pos)]
        elif line.startswith('deal into new stack'):
            instr += [lambda pos: reverse(pos)]
        elif line.startswith('cut '):
            n = int(line[len('cut '):])
            if n < 0:
                n += deck_size
            instr += [lambda pos, n=n: cut(n, pos)]
        else:
            print('Unknown line: "' + line.strip() + '"')
            continue
        itext += [line.strip()]

"""
def interpret(v):
    vals = [0] * deck_size
    for i, x in enumerate(v):
        vals[x] = i
    print(vals)

v = list(range(10))
for i in range(len(instr)-1, -1, -1):
    for x in range(10):
        v[x] = instr[i](v[x])

    print(itext[i])
    #interpret(v)
print(v)
"""

pos = 2020
# pos = 8379

last = pos

pattern = {}
for rep in range(40):
    for i in instr[::-1]:
        pos = i(pos)
    if pos in pattern:
        print('pattern', pos, 'already seen at', pattern[pos], 'now', rep)
    else:
        pattern[pos] = rep
    print((rep+1), ':\t', pos)
    print('diff:', (pos - last) % deck_size)
    last = pos

print(pos)
nshuffles = 101741582076661
