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

    def i_output(self, op, params, output_fn):
        v = self.get_param(params[0], op.pmode[0])
        self.output += [v]
        if output_fn:
            output_fn(v)

    def i_jumptrue(self, op, params):
        v = self.get_param(params[0], op.pmode[0])
        p = self.get_param(params[1], op.pmode[1])
        if v != 0:
            self.pos = p

    def i_jumpfalse(self, op, params):
        v = self.get_param(params[0], op.pmode[0])
        p = self.get_param(params[1], op.pmode[1])
        if v == 0:
            self.pos = p

    def i_lessthan(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        if a < b:
            res = 1
        else:
            res = 0
        self.state[params[2]] = res

    def i_equals(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        if a == b:
            res = 1
        else:
            res = 0
        self.state[params[2]] = res

    def run(self, input_fn, output_fn=None):
        self.output = []

        instr = {
            99: Instr(0, None),
            1: Instr(3, lambda op, params: self.i_add(op, params)),
            2: Instr(3, lambda op, params: self.i_mult(op, params)),
            3: Instr(1, lambda op, params: self.i_input(op, params, input_fn)),
            4: Instr(1, lambda op, params: self.i_output(op, params, output_fn)),
            5: Instr(2, lambda op, params: self.i_jumptrue(op, params)),
            6: Instr(2, lambda op, params: self.i_jumpfalse(op, params)),
            7: Instr(3, lambda op, params: self.i_lessthan(op, params)),
            8: Instr(3, lambda op, params: self.i_equals(op, params))
        }

        self.pos = 0
        while True:
            op = self.state[self.pos]
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
            opos = self.pos
            self.pos += i.numparam + 1

            i.fun(
                Op(opos, opcode, pmode),
                self.state[opos + 1: opos + i.numparam + 1]
            )

        return True
