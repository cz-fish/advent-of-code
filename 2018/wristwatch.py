from typing import Dict, List, Tuple

class WristwatchComputer:
    def __init__(self):
        self.reg = [0, 0, 0, 0]
    
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
    
    def run(self, program: List[Tuple[int, int, int, int]], instr_map: Dict[int, str]):
        for instruction in program:
            opnum, s1, s2, dst = instruction
            assert opnum in instr_map
            opcode = instr_map[opnum]
            self.step((opcode, s1, s2, dst))
