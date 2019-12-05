from collections import namedtuple

Instr = namedtuple('Instr', ['numparam', 'fun'])
Op = namedtuple('Op', ['pos', 'opcode', 'pmode'])


class IntCode:
    def __init__(self, program):
        self.state = program[:]

    def get_param(self, val, pmode):
        if pmode:
            return val
        else:
            return self.state[val]

    def i_add(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        r = a + b
        self.state[params[2]] = r

    def i_mult(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        r = a * b
        self.state[params[2]] = r

    def i_input(self, op, params, input_fn):
        v = input_fn()
        self.state[params[0]] = v

    def i_output(self, op, params):
        v = self.get_param(params[0], op.pmode[0])
        self.output += [v]
        print(f'Output: {v}')

    def run(self, input_fn):
        self.output = []

        instr = {
            99: Instr(0, None),
            1: Instr(3, lambda op, params: self.i_add(op, params)),
            2: Instr(3, lambda op, params: self.i_mult(op, params)),
            3: Instr(1, lambda op, params: self.i_input(op, params, input_fn)),
            4: Instr(1, lambda op, params: self.i_output(op, params))
        }

        pos = 0
        while True:
            op = self.state[pos]
            opcode = op % 100
            pmode = [
                (op // 100) % 10,
                (op // 1000) % 10,
                (op // 10000) % 10
            ]

            if opcode == 99:
                break

            if opcode not in instr:
                return False

            i = instr[opcode]
            i.fun(Op(pos, opcode, pmode), self.state[pos + 1: pos + i.numparam + 1])

            pos += i.numparam + 1

        return True
