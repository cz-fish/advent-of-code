#!/usr/bin/python3.8

from aoc import Env, Integers
from wristwatch import WristwatchComputer

e = Env(19)
e.T("""#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""", 6, 6)


def parse_program(input):
    ip = None
    program = []
    for ln in input.get_valid_lines():
        if ln.startswith('#ip '):
            assert ip is None, f"instruction pointer given twice - previous {ip}, now {ln}"
            ip = int(ln[4:])
        else:
            parts = ln.split(' ')
            assert len(parts) == 4, f"wrong instruction format {ln}"
            program.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    assert ip is not None, "Expected instruction pointer declaration, but didn't find it!"
    return ip, program


def part1(input):
    ip, program = parse_program(input)
    comp = WristwatchComputer(ip)
    comp.run(program, False, None)
    return comp.reg[0]


#e.run_tests(1, part1)
#e.run_main(1, part1)

"""
tail of part 1

6297703 5       [888, 0, 887, 887, 5, 887]      ('addr', 1, 4, 4)       [888, 0, 887, 887, 5, 887]
6297704 6       [888, 0, 887, 887, 6, 887]      ('addi', 4, 1, 4)       [888, 0, 887, 887, 7, 887]
6297705 8       [888, 0, 887, 887, 8, 887]      ('addi', 5, 1, 5)       [888, 0, 887, 887, 8, 888]
6297706 9       [888, 0, 887, 887, 9, 888]      ('gtrr', 5, 2, 1)       [888, 1, 887, 887, 9, 888]
6297707 10      [888, 1, 887, 887, 10, 888]     ('addr', 4, 1, 4)       [888, 1, 887, 887, 11, 888]
6297708 12      [888, 1, 887, 887, 12, 888]     ('addi', 3, 1, 3)       [888, 1, 887, 888, 12, 888]
6297709 13      [888, 1, 887, 888, 13, 888]     ('gtrr', 3, 2, 1)       [888, 1, 887, 888, 13, 888]
6297710 14      [888, 1, 887, 888, 14, 888]     ('addr', 1, 4, 4)       [888, 1, 887, 888, 15, 888]
6297711 16      [888, 1, 887, 888, 16, 888]     ('mulr', 4, 4, 4)       [888, 1, 887, 888, 256, 888]
Day 19 Part 1: 888
"""

def part2(input):
    ip, program = parse_program(input)
    comp = WristwatchComputer(ip)
    comp.reg[0] = 1
    # This only rewrites the program into a more readable form (see below)
    for expl in comp.explain_program(program):
        print(expl)
    # ... but we're not going to run the program, because it would take too long
    #comp.run(program)
    #return comp.reg[0]

    # Analytical solution for both parts. Full explanation of the program at the bottom
    # Given the algorithm explained below is always the same, just with different constants,
    # extract the constants from thse interesting instructions: 17, 20, 21, 23, 31
    # and actually implement a solver that will calculate the constant value and factorization
    parameters = [
        program[17][2], # [17] C + _x -> C
        program[20][2], # [20] C * _x -> C
        program[21][2], # [21] B + _x -> B
        program[23][2], # [23] B + _x -> B
        program[31][2], # [31] B * _x -> B
    ]

    a, b, c, d, e = parameters
    part1_magic_value = a * a * 19 * b + c * 22 + d
    part2_magic_value = part1_magic_value + (27 * 28 + 29) * 30 * e * 32

    print(f"paramters: {parameters}")

    divisors = Integers.all_divisors(part1_magic_value)
    print(f"Part 1: magic: {part1_magic_value}, divisors {divisors}, result: {sum(divisors)}")
    divisors = Integers.all_divisors(part2_magic_value)
    print(f"Part 2: magic: {part2_magic_value}, divisors {divisors}, result: {sum(divisors)}")


#e.run_tests(2, part2)
e.run_main(2, part2)

"""
A: 1, B: 0, C: 0, D: 0, IP: 0, E: 0
[0]     jmp IP + 16 (+1)
[1]     1 -> D
[2]     1 -> E
[3]     D * E -> B
[4]     B == C ? -> B
[5]     jmp B + IP (+1)
[6]     jmp IP + 1 (+1)
[7]     D + A -> A
[8]     E + 1 -> E
[9]     E > C ? -> B
[10]    jmp IP + B (+1)
[11]    jmp 2 (+1)
[12]    D + 1 -> D
[13]    D > C ? -> B
[14]    jmp B + IP (+1)
[15]    jmp 1 (+1)
[16]    jmp IP * IP (+1)
[17]    C + 2 -> C
[18]    C * C -> C
[19]    IP * C -> C
[20]    C * 11 -> C
[21]    B + 2 -> B
[22]    B * IP -> B
[23]    B + 7 -> B
[24]    C + B -> C
[25]    jmp IP + A (+1)
[26]    jmp 0 (+1)
[27]    IP -> B
[28]    B * IP -> B
[29]    IP + B -> B
[30]    IP * B -> B
[31]    B * 14 -> B
[32]    B * IP -> B
[33]    C + B -> C
[34]    0 -> A
[35]    jmp 0 (+1)

-----
initialization (instructions 17 to 35):

C = 2 * 2 * 19 * 11 (=836)
B = 2 * 22 + 7 (=51)
C = 836 + 51 = 887
if part2:
    B = (27 * 28 + 29) * 30 * 14 * 32 (=10550400)
    C = 887 + 10550400 (=10551287)
A = 0 (reset result. Initial value 1 was only used for the above 'if')

-----
loops: (instructions 1 to 16, equivalent program):

for (D = 1; D <= C; D++):
    for (E = 1; E <= C; E++):
        if D * E == C:
            A += D

A is the result.

-----
analysis:

A is the sum of all factors of C.
In part1, C = 887, which is prime, so the only factors are 1, 887. Therefore A = 888
In part2, C = 10551287. Prime factors 127, 251, 331. Result = 1 + 127 + 251 + 331 + 31877 + 42037 + 83081 + 10551287 = 10708992
"""
