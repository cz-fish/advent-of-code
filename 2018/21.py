#!/usr/bin/python3.8

from pyaoc import Env
from wristwatch import parse_program, WristwatchComputer

e = Env(21)

def loader():
    b = 0
    c = 65536
    e = 7586220
    while True:
        # instr 8
        b = c & 255
        e += b
        e &= 16777215
        e *= 65899
        e &= 16777215
        #print(f"b={b}, c={c}, e={e}")
        if c < 256:
            # instr 28
            # This is the first time the program can reach the halting
            # instruction. It will halt if register a == register e,
            # so the current value in register e is the value that
            # the register a should have for the program to stop after
            # the minimal number of cycles.
            return e
        c = c // 256


def part1(input):
    """
    What is the lowest non-negative integer value for register 0 that causes
    the program to halt after executing the fewest instructions?
    """
    # Load and print the program for reference
    ip, program = parse_program(input.get_valid_lines())
    comp = WristwatchComputer(ip)
    for ln in comp.explain_program(program):
        print(ln)
    print('------------')
    # Loader is a reimplementation of the input program
    return loader()


e.run_main(1, part1)


def loader2():
    # At the end of each loop (instr 28), the program will compare register e with
    # register a. When they're not equal, the program does one more iteration of the
    # outer loop, modifying the value of e. At some point, the value of 'e' will start
    # to repeat. At that point, the program will have an infinite cycle and never halt.
    # What we want to return is the last value of 'e' just before the program would
    # start looping forever. Setting 'a' to that last value of 'e' would result in the
    # highest number of cycles, while the program is still also able to halt.
    counter = 0
    used_cs = {}
    last_e = None

    b = 0
    e = 0
    while True:
        c = e | 65536
        if c in used_cs:
            print(f"repeated 'c' value {c} was first seen after {used_cs[c]} loops, now {counter} loops")
            return last_e
        used_cs[c] = counter
        e = 7586220
        break_inner = False
        while True:
            # instr 8
            b = c & 255
            e += b
            e &= 16777215
            e *= 65899
            e &= 16777215
            if c < 256:
                # instr 28
                counter += 1
                last_e = e
                break_inner = True
            if break_inner:
                break
            c = c // 256


def part2(input):
    """
    What is the lowest non-negative integer value for register 0 that causes
    the program to halt after executing the most instructions?
    """
    # The program is the same as in part 1, no need to print it out again
    # Loader2 is a reimplementation of the program
    return loader2()


e.run_main(2, part2)

# printout of the program with symbolic names
"""
A: 0, B: 0, IP: 0, C: 0, D: 0, E: 0
[0]     123 -> E
[1]     E & 456 -> E
[2]     E == 72 ? -> E
[3]     jmp E + IP (+1)
[4]     jmp 0 (+1)
[5]     0 -> E
[6]     E | 65536 -> C
[7]     7586220 -> E
loop start
[8]     C & 255 -> B
[9]     E + B -> E
[10]    E & 16777215 -> E
[11]    E * 65899 -> E
[12]    E & 16777215 -> E
[13]    256 > C ? -> B
[14]    jmp B + IP (+1)
[15]    jmp IP + 1 (+1)
[16]    jmp 27 (+1)
[17]    0 -> B
  inner loop begin
[18]    B + 1 -> D
[19]    D * 256 -> D
[20]    D > C ? -> D
[21]    jmp D + IP (+1)
[22]    jmp IP + 1 (+1)
[23]    jmp 25 (+1)    # break inner
[24]    B + 1 -> B
[25]    jmp 17 (+1)
  inner loop end
[26]    B -> C
[27]    jmp 7 (+1)
loop end
[28]    E == A ? -> B
[29]    jmp B + IP (+1)
[30]    jmp 5 (+1)
"""
