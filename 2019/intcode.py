from collections import namedtuple

Instr = namedtuple('Instr', ['numparam', 'fun'])
Op = namedtuple('Op', ['pos', 'opcode', 'pmode'])


class IntCode:
    def __init__(self, program):
        self.state = program[:]
        self.memory = {}

    def memory_get(self, pos):
        if pos < len(self.state):
            return self.state[pos]
        return self.memory.get(pos, 0)

    def memory_put(self, pos, val):
        if pos < len(self.state):
            self.state[pos] = val
        self.memory[pos] = val

    def get_param(self, param, pmode):
        if pmode == 1:
            return param
        elif pmode == 2:
            return self.memory_get(self.relbase + param)
        else:
            return self.memory_get(param)
    
    def set_param(self, param, pmode, val):
        if pmode == 2:
            self.memory_put(self.relbase + param, val)
        elif pmode == 0:
            self.memory_put(param, val)

    def i_add(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        r = a + b
        self.set_param(params[2], op.pmode[2], r)

    def i_mult(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        r = a * b
        self.set_param(params[2], op.pmode[2], r)

    def i_input(self, op, params, input_fn):
        v = input_fn()
        self.set_param(params[0], op.pmode[0], v)

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
        self.set_param(params[2], op.pmode[2], res)

    def i_equals(self, op, params):
        a = self.get_param(params[0], op.pmode[0])
        b = self.get_param(params[1], op.pmode[1])
        if a == b:
            res = 1
        else:
            res = 0
        self.set_param(params[2], op.pmode[2], res)

    def i_relbase(self, op, params):
        val = self.get_param(params[0], op.pmode[0])
        self.relbase += val

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
            8: Instr(3, lambda op, params: self.i_equals(op, params)),
            9: Instr(1, lambda op, params: self.i_relbase(op, params))
        }

        self.pos = 0
        self.relbase = 0
        while True:
            op = self.memory_get(self.pos)
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

            params = []
            for j in range(opos + 1, opos + i.numparam + 1):
                params += [self.memory_get(j)]
            i.fun(
                Op(opos, opcode, pmode),
                params
            )

        return True
