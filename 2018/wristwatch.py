from typing import Dict, List, Tuple

"""
Addition:

addr (add register) stores into register C the result of adding register A and register B.
addi (add immediate) stores into register C the result of adding register A and value B.
Multiplication:

mulr (multiply register) stores into register C the result of multiplying register A and register B.
muli (multiply immediate) stores into register C the result of multiplying register A and value B.
Bitwise AND:

banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
Bitwise OR:

borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
Assignment:

setr (set register) copies the contents of register A into register C. (Input B is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)
Greater-than testing:

gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
Equality testing:

eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
"""

# 4 registers used on day 16
# expanded to 6 on day 19
NUM_REGISTERS = 6

class WristwatchComputer:
    def __init__(self, instr_ptr=None):
        self.reg = [0] * NUM_REGISTERS
        if instr_ptr is None:
            # On day 16, we are not given instruction pointer
            # register. Use 5, which is free, because day 16
            # only has 4 registers
            self.ip_index = NUM_REGISTERS - 1
        else:
            self.ip_index = instr_ptr
    
    @classmethod
    def all_instructions(cls):
        return [
            "addr", "addi",
            "mulr", "muli",
            "banr", "bani",
            "borr", "bori",
            "setr", "seti",
            "gtir", "gtri", "gtrr",
            "eqir", "eqri", "eqrr",
        ]

    def set_regs(self, reg: List[int]):
        assert len(reg) <= NUM_REGISTERS, f"Too many registers given: {len(reg)}, max {NUM_REGISTERS}"
        # If fewer than NUM_REGISTERS provided, pad with zeroes
        self.reg = (reg + [0] * NUM_REGISTERS)[:NUM_REGISTERS]

    def step(self, instruction: Tuple[str, int, int, int]):
        op, s1, s2, dst = instruction

        first = self.reg[s1]
        if op[3] == 'i':
            second = s2
        elif op[3] == 'r':
            second = self.reg[s2]

        val = None
        if op[0] == 'a':
            val = first + second
        elif op[0] == 'm':
            val = first * second
        elif op[0] == 'b':
            if op[1] == 'a':
                val = first & second
            elif op[1] == 'o':
                val = first | second
        elif op[0] == 's':
            if op[3] == 'i':
                first = s1
            val = first
        elif op[0] in 'eg':
            if op[2] == 'i':
                first = s1
            if op[0] == 'g':
                val = 1 if first > second else 0
            else:
                val = 1 if first == second else 0
        else:
            assert False, f"Invalid opcode {op}, instruction {instruction}"
        
        if val is None:
            assert False, f"Invalid instruction {instruction}"

        self.reg[dst] = val
        # increment instruction pointer
        self.reg[self.ip_index] += 1
    
    def run(self, program: List[Tuple[int, int, int, int]], instr_map: Dict[int, str]):
        self.reg[self.ip_index] = 0
        while self.reg[self.ip_index] >= 0 and self.reg[self.ip_index] < len(program):
            opnum, s1, s2, dst = program[self.reg[self.ip_index]]
            assert opnum in instr_map
            opcode = instr_map[opnum]
            self.step((opcode, s1, s2, dst))
