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

IntInstruction = Tuple[int, int, int, int]
Instruction = Tuple[str, int, int, int]
IntProgram = List[IntInstruction]
Program = List[Instruction]

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

    def step(self, instruction: Tuple[str, int, int, int]) -> str:
        op, s1, s2, dst = instruction

        effect = str(self.reg) + "\t" + str(instruction) + "\t"

        if op == 'seti' or op[2] == 'i':
            # seti, gtir, eqir have s1 as a value
            first = s1
        else:
            # all other instructions treat it as register
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
            val = first
        elif op[0] in 'eg':
            if op[0] == 'g':
                val = 1 if first > second else 0
            else:
                val = 1 if first == second else 0
        else:
            assert False, f"Invalid opcode {op}, instruction {instruction}"
        
        if val is None:
            assert False, f"Invalid instruction {instruction}"

        self.reg[dst] = val
        effect += str(self.reg)
        return effect
    
    def run_with_mapping(self, program: IntProgram, instr_map: Dict[int, str]):
        # Run program where instruction opcodes are encoded as integers with
        # a dictionary provided.

        # Translate opnums to opcodes and then just run normally.
        real_program = []
        for opnum, s1, s2, dst in program:
            assert opnum in instr_map
            opcode = instr_map[opnum]
            real_program.append((opcode, s1, s2, dst))
        self.run(real_program)
    
    def run(self, program: Program, print_as_you_go=False, break_after=None):
        instrptr = 0
        cycles = 0
        while instrptr >= 0 and instrptr < len(program):
            # update instruction pointer register
            self.reg[self.ip_index] = instrptr
            opcode, s1, s2, dst = program[instrptr]
            effect = self.step((opcode, s1, s2, dst))
            if print_as_you_go:
                print(f"{cycles}\t{instrptr}\t{effect}")
            instrptr = self.reg[self.ip_index] + 1
            cycles += 1
            if break_after is not None and cycles == break_after:
                break
        return cycles

    def explain_instruction(self, instruction: Instruction) -> str:
        op, s1, s2, dst = instruction

        reg_map = self.get_register_map()

        if op == 'seti' or op[2] == 'i':
            # seti, gtir, eqir have s1 as a value
            first = str(s1)
        else:
            # all other instructions treat it as register
            first = reg_map[s1]
        
        if op[3] == 'i':
            second = str(s2)
        elif op[3] == 'r':
            if s2 not in reg_map:
                second = '_'
            else:
                second = reg_map[s2]

        expr = None
        if op[0] == 'a':
            expr = f"{first} + {second}"
        elif op[0] == 'm':
            expr = f"{first} * {second}"
        elif op[0] == 'b':
            if op[1] == 'a':
                expr = f"{first} & {second}"
            elif op[1] == 'o':
                expr = f"{first} | {second}"
        elif op[0] == 's':
            expr = first
        elif op[0] in 'eg':
            if op[0] == 'g':
                expr = f"{first} > {second} ?"
            else:
                expr = f"{first} == {second} ?"
        else:
            assert False, f"Invalid opcode {op}, instruction {instruction}"
        
        if expr is None:
            assert False, f"Invalid instruction {instruction}"

        if dst == self.ip_index:
            return f"jmp {expr} (+1)"
        else:
            return f"{expr} -> {reg_map[dst]}"

    def get_register_map(self) -> Dict[int, str]:
        # Map register numbers to letters A..E, skipping the register that represents the instruction pointer
        reg_map = dict(zip([i for i in range(NUM_REGISTERS) if i != self.ip_index], [chr(ord('A') + x) for x in range(NUM_REGISTERS - 1)]))
        # Name the instruction pointer register IP
        reg_map[self.ip_index] = "IP"
        return reg_map

    def explain_program(self, program: Program) -> List[str]:
        reg_map = self.get_register_map()
        return [', '.join([f"{reg_map[i]}: {self.reg[i]}" for i in range(NUM_REGISTERS)])] + \
            [f"[{i}]\t" + self.explain_instruction(instr) for i, instr in enumerate(program)]


def parse_program(lines):
    ip = None
    program = []
    for ln in lines:
        if ln.startswith('#ip '):
            assert ip is None, f"instruction pointer given twice - previous {ip}, now {ln}"
            ip = int(ln[4:])
        else:
            parts = ln.split(' ')
            assert len(parts) == 4, f"wrong instruction format {ln}"
            program.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    assert ip is not None, "Expected instruction pointer declaration, but didn't find it!"
    return ip, program
