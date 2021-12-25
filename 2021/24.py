#!/usr/bin/python3.8

from aoc import Env

e = Env(24)

L = 14

"""
Assembly analysis

There are 14 blocks of 18 instructions each. Each block works on one input digit, but takes a carry value from
the previous digit. Each block has the same instructions and only 3 of them have varying parameters
(key variables - we'll denote them A, B, C).
Because the instructions are the same for every digit, some of them are nops for the first digit.

The 'carry' from the previous digit, modulo 26 + B is compared against the current digit. For values of B
greater than 9, this can never match, so it is guaranteed that for those digits the program will take
branch a). For other values of B, there is a digit such that the values will match and the program will
take branch b) instead.

Branch a) increases the value of 'carry', which we require to be 0 at the end of the program, while branch
b) keeps or reduces the 'carry' instead, so in order to reach 'carry' = 0 at the end, we want to take branch
b) when possible (that means trying to match the digit to 'carry' % 26+B

In branch a), 'carry' is multiplied by 26 and the value of C is added to the 'carry'. This is effectively
a stack, where each item is one digit of a base-26. The digits where Z = 1 push into the stack, and the
digits where Z = 26 pop from the stack. Notice that there is the same amount of Z=1 as Z=26 in the input.
These form pairs in a last-in-first-out order, and from each pair, we get a formula that will give us the
values of 2 digits of the model number.

The formula is
Di - Aj = Dj + Bi
where Di and Dj are i-th and j-th digits (j < i, meaning that j is more significant digit)
Aj is the A coefficient of j-th digit, and Bi is B coefficient of i-th digit.
(Note that A of the digits where Z=1 and B of the digits where Z=26 are not used in the calculation)

we get Di = Dj + Aj + Bi, where we want to either maximize (part 1) or minimize (part 2) both Di and Dj,
while they must both be within 0 < D <= 9.

Once we have constructed all 14 digits of the number, we run the program once just to verify that it
indeed ends with checksum being 0.
"""


def analyze_program(program):
    digit = -1
    instr = []
    var = []
    val = [[] for _ in range(14)]
    c = 0
    for ln in program:
        x = ln.split(' ')
        i = x[0]
        a = x[1]
        if len(x) > 2:
            b = x[2]
        else:
            b = None
        if i == 'inp':
            digit += 1
            c = -1
        c += 1
        if digit == 0:
            instr += [i]
            var += [a]
        else:
            assert instr[c] == i
            assert var[c] == a
        val[digit] += [b]
    
    for i, j in enumerate(val):
        s = ', '.join(str(x) for x in j)
        Z = j[4]
        A = j[5]
        B = j[15]
        print(f"digit {i:02} [{Z:2}, {A:2}, {B:2}]  {s}")
        

def get_key_variables(program):
    assert len(program) == L * 18
    A = []
    B = []
    C = []
    for i in range(L):
        # div z 1 (or 26)
        s, t, v = program[i * 18 + 4].split(' ')
        assert s == 'div' and t == 'z'
        A += [int(v)]
        assert A[-1] == 1 or A[-1] == 26
        # add x VAL
        s, t, v = program[i * 18 + 5].split(' ')
        assert s == 'add' and t == 'x'
        B += [int(v)]
        # add y VAL
        s, t, v = program[i * 18 + 15].split(' ')
        assert s == 'add' and t == 'y'
        C += [int(v)]
    return A, B, C


def solve(A, B, C, highest):
    res = [0] * L
    st = []
    for i in range(L):
        if A[i] == 1:
            st.append((i, C[i]))
        elif A[i] == 26:
            assert st
            j, w = st.pop()
            # Di = Dj + w + Bi = Dj + x
            # maximize or minimize Dj so that both Di and Dj are within 0 < D <= 9
            x = w + B[i]
            assert -8 <= x <= 8
            if highest:
                Dj = min(9, 9 - x)
                Di = Dj + x
            else:
                Dj = max(1, 1 - x)
                Di = Dj + x
            assert 0 < Di <= 9
            assert 0 < Dj <= 9
            res[i] = Di
            res[j] = Dj
        else:
            assert False
    assert not st
    return res


def run_program(lines, inputs):
    reg = [0, 0, 0, 0]
    pos = 0
    for ln in lines:
        x = ln.split(' ')
        r = ord(x[1]) - ord('w')
        if x[0] == 'inp':
            # print(pos, reg)
            reg[r] = inputs[pos]
            pos += 1
        else:
            if x[2] >= 'w' and x[2] <= 'z':
                t = reg[ord(x[2]) - ord('w')]
            else:
                t = int(x[2])

            if x[0] == 'add':
                reg[r] = reg[r] + t
            elif x[0] == 'mul':
                reg[r] = reg[r] * t
            elif x[0] == 'div':
                assert t != 0
                reg[r] = reg[r] // t
            elif x[0] == 'mod':
                assert reg[r] >= 0
                assert t > 0
                reg[r] = reg[r] % t
            elif x[0] == 'eql':
                reg[r] = 1 if reg[r] == t else 0
            else:
                assert False
    return reg[3]


def part1(input):
    program = input.get_valid_lines()
    analyze_program(program)
    A, B, C = get_key_variables(program)
    highest = solve(A, B, C, True)
    check = run_program(program, highest)
    n = ''.join(str(x) for x in highest)
    if check == 0:
        return n
    else:
        return None
#    number = [9, 1, 3, 9, 8, 2, 9, 9, 6, 9, 7, 9, 9, 6]


e.run_main(1, part1)


def part2(input):
    program = input.get_valid_lines()
    # analyze_program(program)
    A, B, C = get_key_variables(program)
    lowest = solve(A, B, C, False)
    check = run_program(program, lowest)
    n = ''.join(str(x) for x in lowest)
    if check == 0:
        return n
    else:
        return None
#    number = [4, 1, 1, 7, 1, 1, 8, 3, 1, 4, 1, 2, 9, 1]


e.run_main(2, part2)

"""
read digit

set x to carry % 26

div carry by Z ( either by 1 (keep) or by 26)

add A to x
if x != digit:
    x = 1
else:
    x = 0

set y to 25
multiply y by x (=1 or 0)
add 1 to y (=1 or 26)

multiply carry by y

copy digit to y
add B to y

multiply y by x (=1 or 0)

add y to carry


------------

digit0, carry0 -> (blackbox Z, A, B) -> digit1, carry1


if digit != (carry % 26) + A:
    carry /= Z
    carry *= 26
    carry += digit + B
else:
    carry /= Z


------

D0 == 0 + 12: false
carry1 = D0 + 4

D1 == D0 + 4 + 11: false
carry2 = (D0 + 4) * 26 + D1 + 10

D2 == (carry2) % 26 + 14: false
carry3 = ((D0 + 4) * 26 + D1 + 10) * 26 + D2 + 12

D3 == (carry3) % 26 - 6:

carry3 % 26 = D3 + 6, ideally 9 + 6 = 15
carry3 % 26 == 15
carry3 = 15 + 26x
A * 26 + D2 + 12 = 15 + 26 * x
D2 = 3
D3 = 9

--------------
carry 357 = (D0 + 4) * 26 + D1 + 10

9 - -6 -> 15
15 - 12 -> 3

9 - -9 -> 18
18 - 16 -> 2

9 - -5 -> 14
14 - 8 -> 6

9 - -9 -> 18
18 - 7 -> 11
7 - -9 -> 16
16 - 7 -> 9

9 - -5 -> 14
14 - 6 -> 8

5 - -5 -> 10
10 - 1 -> 9

9 - -2 -> 11
11 - 
----------

F - (A) - B' -> valid digit, ideally 9


-6 match to 12
F - (-6) - 12 = d
F + 6 - 12 = d
F - 6 = d
F = d + 6
maximize d so that F is >=1 <=9
d = 3
F = 9

F = d + B' + A

-6, 12
F = d + 12 - 6 = d + 6
-> 12 maps to 3
-> -6 maps to 9

-9, 16
F = d + 16 - 9 = d + 7
-> 16 maps to 2
-> -9 maps to 9

-5, 8
F = d + 8 - 5 = d + 3
-> 8 maps to 6
-> -5 maps to 9

-9, 7
F = d + 7 - 9 = d - 2
-> 7 maps to 9
-> -9 maps to 7

-5, 6
F = d + 6 - 5 = d + 1

-2, 10
F = d + 10 - 2 = d + 8

-7, 4
F = d + 4 - 7 = d - 3

last 5 digits: z divided by 26**5 = 11881376 if digits match

------------

-6, 12
F = d + 12 - 6 = d + 6
d = 1
F = 7

-9, 16
F = d + 16 - 9 = d + 7
d = 1
F = 8

-5, 8
F = d + 8 - 5 = d + 3
d = 1
F = 4

-9, 7
F = d + 7 - 9 = d - 2
d = 3
F = 1

-5, 6
F = d + 6 - 5 = d + 1
d = 1
F = 2

-2, 10
F = d + 10 - 2 = d + 8
d = 1
F = 9

-7, 4
F = d + 4 - 7 = d - 3
d = 4
F = 1
"""

