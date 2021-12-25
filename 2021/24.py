#!/usr/bin/python3.8

from aoc import Env

e = Env(24)


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
        

def run_program(lines, inputs):
    reg = [0, 0, 0, 0]
    pos = 0
    for ln in lines:
        x = ln.split(' ')
        r = ord(x[1]) - ord('w')
        if x[0] == 'inp':
            print(pos, reg)
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
    #number = [9, 9, 3, 9, 9, 2, 9, 9, 6, 9, 7, 5, 9, 9]
    number = [9, 1, 3, 9, 8, 2, 9, 9, 6, 9, 7, 9, 9, 6]
    val = run_program(program, number)
    n = ''.join(str(x) for x in number)
    if val == 0:
        return f"SUCCESS: {n} -> {val}"
    else:
        return f"FAILURE: {n} -> {val}"
    return 0


#e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    program = input.get_valid_lines()
    #analyze_program(program)
    #number = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    number = [4, 1, 1, 7, 1, 1, 8, 3, 1, 4, 1, 2, 9, 1]
    val = run_program(program, number)
    n = ''.join(str(x) for x in number)
    if val == 0:
        return f"SUCCESS: {n} -> {val}"
    else:
        return f"FAILURE: {n} -> {val}"
    return 0


# e.run_tests(2, part2)
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

