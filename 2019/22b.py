#!/usr/bin/python3.8

#deck_size = 10007
#deck_size = 10
deck_size = 119315717514047
shuffles = 101741582076661


itext = []

# npos = a * pos + b (mod size)
a = 1
b = 0

with open('input22.txt', 'rt') as f:
    for line in f.readlines():
        if line.startswith('deal with increment '):
            n = int(line[len('deal with increment '):])
            # npos = n * pos + 0 (mod size)
            a = a * pow(n, -1, deck_size)
        elif line.startswith('deal into new stack'):
            # npos = -pos - 1 (mod size)
            a, b = -a, b - a
        elif line.startswith('cut '):
            n = int(line[len('cut '):])
            b = b + n * a
        else:
            print('Unknown line: "' + line.strip() + '"')
            continue
        itext += [line.strip()]
        a = a % deck_size
        b = b % deck_size

print(f"npos = {a} * pos + {b}")
# print((a * 8379 + b) % deck_size)

# what ends on position X after 1 iteration?
# a * X + b
# (back-tested against result of part 1)

# what ends on position X after N iterations?
#     a * (a * (a * ... (a * X + b) ... + b) + b) + b
# => A = a ** N
# => B = a**(N-1) * b + a**(N-2) * b + ... a**2 * b + a * b + b =
#      = b * (a**(N-2) + ... + a + 1) =
#      = b * (a**N - 1) / (a - 1)

A = pow(a, shuffles, deck_size)
B = (b * (A - 1) * pow(a-1, -1, deck_size)) % deck_size

print((A * 2020 + B) % deck_size)
