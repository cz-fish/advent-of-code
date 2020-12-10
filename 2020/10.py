#!/usr/bin/python3.8

from aoc import Input

inp = Input('input10.txt', ["""16
10
15
5
1
11
7
19
6
12
4
""",
"""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""])

# inp.use_test(0)
# exp = 7 * 5
# inp.use_test(1)
# exp = 22 * 10

nums = sorted(inp.get_ints())
out = nums[-1] + 3
print(f"Device joltage: {out}")
anums = [0] + nums + [out]

ones = 0
threes = 0

for i, n in enumerate(anums[:-1]):
    x = anums[i + 1]
    d = x - n
    assert(d > 0 and d < 4)
    if d == 1:
        ones += 1
    elif d == 3:
        threes += 1
print(f"Part 1: ones {ones}, threes {threes}, multiplied {ones * threes}")

### Part 2

jolt = [0] * (out + 1)
jolt[0] = 1
for adap in anums[1:]:
    count = 0
    for i in [-3, -2, -1]:
        x = adap + i
        if x < 0:
            continue
        count += jolt[x]
    jolt[adap] = count

print(f"Part 2: {jolt[-1]}")
