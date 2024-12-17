#!/usr/bin/python3.12

from pyaoc import Env
import re
from collections import deque

e = Env(17, param=0)
e.T("""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""", "4,6,3,5,6,3,5,2,1,0", None)

e.T("""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""", None, 117440, param=117440)

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7
REG_A = 0
REG_B = 1
REG_C = 2


def pretty_opcode(opcode, operand):
    mnemo, combo = {
        0: ("ADV", True),
        1: ("BXL", False),
        2: ("BST", True),
        3: ("JNZ", False),
        4: ("BXC", False),
        5: ("OUT", True),
        6: ("BDV", True),
        7: ("CDV", True),
    }[opcode]
    if not combo or operand < 4:
        opstr = str(operand)
    else:
        opstr = f"[{chr(ord('A') + operand - 4)}]"
    return f"{mnemo} {opstr}".ljust(7, ' ')


def pretty_regs(regs):
    nums = [oct(v)[2:].rjust(10, ' ') for v in regs]
    return ' '.join(nums)


class Computer:
    def __init__(self, regs, instr):
        assert len(regs) == 3
        self.regs = regs[:]
        assert all([i >=0 and i <= 7 for i in instr])
        self.instr = instr[:]

    def combo_operand(self, op):
        if op >= 0 and op <= 3:
            return op
        if op >= 4 and op <= 6:
            return self.regs[op - 4]
        assert False, f"Invalid combo operand {op}"

    def run_to_halt(self) -> str:
        self.pc = 0
        out = []
        while self.pc < len(self.instr):
            opcode = self.instr[self.pc]
            operand = self.instr[self.pc + 1]
            self.pc += 2
            if opcode == ADV or opcode == BDV or opcode == CDV:
                # right shift
                num = self.regs[REG_A] >> self.combo_operand(operand)
                target = { ADV: REG_A, BDV: REG_B, CDV: REG_C }[opcode]
                self.regs[target] = num
            elif opcode == BXL:
                # xor with literal
                self.regs[REG_B] = self.regs[REG_B] ^ operand
            elif opcode == BST:
                # store b
                self.regs[REG_B] = self.combo_operand(operand) % 8
            elif opcode == JNZ:
                # jump
                if self.regs[REG_A]:
                    self.pc = operand
            elif opcode == BXC:
                # xor registers
                self.regs[REG_B] = self.regs[REG_B] ^ self.regs[REG_C]
            elif opcode == OUT:
                val = self.combo_operand(operand) % 8
                out.append(val)
        return out

    def run_debug(self) -> str:
        self.pc = 0
        out = []
        while self.pc < len(self.instr):
            opcode = self.instr[self.pc]
            operand = self.instr[self.pc + 1]
            pc_before = str(self.pc).rjust(3, ' ')
            regs_before = pretty_regs(self.regs)
            self.pc += 2
            if opcode == ADV or opcode == BDV or opcode == CDV:
                # right shift
                num = self.regs[REG_A] >> self.combo_operand(operand)
                target = { ADV: REG_A, BDV: REG_B, CDV: REG_C }[opcode]
                self.regs[target] = num
            elif opcode == BXL:
                # xor with literal
                self.regs[REG_B] = self.regs[REG_B] ^ operand
            elif opcode == BST:
                # store b
                self.regs[REG_B] = self.combo_operand(operand) % 8
            elif opcode == JNZ:
                # jump
                if self.regs[REG_A]:
                    self.pc = operand
            elif opcode == BXC:
                # xor registers
                self.regs[REG_B] = self.regs[REG_B] ^ self.regs[REG_C]
            elif opcode == OUT:
                val = self.combo_operand(operand) % 8
                out.append(val)
            regs_after = pretty_regs(self.regs)
            print(pc_before, pretty_opcode(opcode, operand), regs_before, "->", regs_after, out)
        return out

    def __repr__(self):
        o = f"[Computer, regs: {self.regs}, instructions: {self.instr}]"
        return o


def parse_input(input):
    groups = input.get_groups()
    num_re = re.compile(r'\d+')
    regs = []
    for ln in groups[0]:
        ln = ln.strip()
        if not ln:
            continue
        nums = num_re.findall(ln)
        assert len(nums) == 1, f"{ln} -> {nums}"
        regs.append(int(nums[0]))
    assert len(regs) == 3
    program = [int(x) for x in num_re.findall(groups[1][0])]
    return Computer(regs, program)


def part1(input):
    computer = parse_input(input)
    #print(computer)
    return ','.join([str(x) for x in computer.run_to_halt()])


e.run_tests(1, part1)
e.run_main(1, part1)

ZERO=0
ONE=1
X=2
NOT=3


def num_to_bits(target_digit):
    return [(target_digit >> 2) & 1, (target_digit >> 1) & 1, target_digit & 1]


def compute_c_lower_bits(B, target):
    C = target ^ B
    #c_bits = num_to_bits(C)
    if B == 5 and C & 1 != 1:
        return None
    if B == 6 and C & 3 != 3:
        return None
    if B == 7 and C & 7 != 7:
        return None
    return C


def mask_apply(mask, array, index):
    out = []
    start_a = index - len(mask)
    for i in range(0, start_a):
        out.append(array[i])
    for i in range(len(mask)):
        v = mask[i]
        if start_a < 0:
            if v != '0':
                return None, False
        else:
            a = array[start_a]
            if a == '.':
                out.append(v)
            elif v == '.':
                out.append(a)
            elif a == v:
                out.append(a)
            else:
                return None, False
        start_a += 1
    for i in range(start_a, len(array)):
        out.append(array[i])
    return out, True


def calculate_a(output):
    bit_length = len(output) * 3
    empty_a = ['.' for _ in range(bit_length)]
    q = deque()
    q.append((0, empty_a[:]))
    solutions = []
    while q:
        pos, a = q.popleft()
        if pos == len(output):
            A = ''.join(['0' if x=='.' else x for x in a])
            solutions.append(int(A, base=2))
            continue
        target_digit = output[pos]
        index = bit_length - pos * 3
        for B in range(8):
            C = compute_c_lower_bits(B, target_digit)
            if C is None:
                continue
            shift = 7 - B
            mask = ['.' for _ in range(shift + 3)]
            mask, match = mask_apply([str(x) for x in num_to_bits(C)], mask, len(mask) - shift)
            assert match
            mask, match = mask_apply([str(x) for x in num_to_bits(B)], mask, len(mask))
            assert match
            new_a, match = mask_apply(mask, a, index)
            if match:
                #print(''.join(new_a))
                q.append((pos + 1, new_a))
                pass
    print(f"Found {len(solutions)} solutions: {solutions}")
    return min(solutions)


def part2(input):
    computer = parse_input(input)
    print(computer)
    A = calculate_a(computer.instr)
    computer.regs[0] = A
    output = computer.run_to_halt()
    print(f"Computer output: {output}, matches expected: {output == computer.instr}")
    return A


#e.run_tests(2, part2)
e.run_main(2, part2)


"""
Program: 0,3,5,4,3,0
ADV 3 (regA >>= 3)
OUT [4] (regA)
JNZ 0

regA = 0 + (3 << 6) + (5 << 9) + (4 << 12) + (3 << 15) = 117440


Program: 2,4,1,7,7,5,0,3,4,0,1,7,5,5,3,0
2,4 BST [4] B = A % 8
1,7 BXL 7   B = B ^ 7
7,5 CDV [5] C = A >> B
0,3 ADV 3   A = A >> 3
4,0 BXC 0   B = B ^ C
1,7 BXL 7   B = B ^ 7
5,5 OUT [5] out (B % 8)
3,0 JNZ 0

    B  sh  pattern      B^C  not
000 0   7  XYZ....000   XYZ  xyz
001 1   6   XYZ...001   XYz  xyZ
010 2   5    XYZ..010   XyZ  xYz
011 3   4     XYZ.011   Xyz  xYZ
100 4   3      XYZ100   xYZ  Xyz
101 5   2       XY101   xY0  Xy1
110 6   1        X110   x01  X10
111 7   0         111   000  111


    B  sh  pattern      ~B    (~B)^C  not  C       C     B           tgt
000 0   7  XYZ....000   111   xyz     XYZ  XYZ    XYZ ^ 000 = XYZ == ABC,  XYZ = ABC ^ 000
001 1   6   XYZ...001   110   xyZ     XYz  XYZ    XYZ ^ 001 = XYz == ABC
010 2   5    XYZ..010   101   xYz     XyZ  XYZ    XYZ ^ 010 = XyZ == ABC
011 3   4     XYZ.011   100   xYZ     Xyz  XYZ    XYZ ^ 011 = Xyz == ABC
100 4   3      XYZ100   011   Xyz     xYZ  XYZ    XYZ ^ 100 = xYZ == ABC
101 5   2       XY101   010   Xy1     xY0  XY1    XY1 ^ 101 = xY0 == ABC
110 6   1        X110   001   X10     x01  X11    X11 ^ 110 = x01 == ABC
111 7   0         111   000   111     000  111    111 ^ 111 = 000 == ABC


267608763605915 too high
246290604621824 too low

258394985014171
111010110000001001000101010010110010001110011011
.........00000.001000101010010110010001110011011
......110000001001000101010010110010001110011011
..101.110000001001000101010010110010001110011011
..1010110000001001000101010010110010001110011011

111100110110001110000101010010110010001110011011
...XX....XX....XXX..............................
  |  |  |  |  |  |  |
15 14 13 12 11 10 09

"""
