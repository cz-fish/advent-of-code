#!/usr/bin/env python3.8

def execute(instr, boot):
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    toggles = {
        'inc': 'dec',
        'dec': 'inc',
        'tgl': 'inc',
        'jnz': 'cpy',
        'cpy': 'jnz',
    }
    registers['a'] = boot
    ip = 0
    iterations = 0
    while True:
        if ip >= len(instr):
            break
        i = instr[ip][:]
        if ip == 2:
            # multiplication shortcut
            print(f'multiply {registers["a"]} x {registers["b"]}')
            v = registers['a'] * registers['b']
            registers['a'] = v
            registers['b'] -= 1
            ip = 11
            continue
        opcode = i[0]
        param = i[1]
        if opcode == 'inc':
            registers[param] += 1
        elif opcode == 'dec':
            registers[param] -= 1
        elif opcode == 'tgl':
            if param >= 'a' and param <= 'd':
                off = registers[param]
            else:
                off = int(param)
            dest = ip + off
            print(f"Toggle at position {dest}")
            if dest < 0 or dest >= len(instr):
                # out of bounds, ignore
                pass
            else:
                instr[dest][0] = toggles[instr[dest][0]]
        elif opcode == 'jnz':
            if param >= 'a' and param <= 'd':
                cond = registers[param]
            else:
                cond = int(param)
            offstr = i[2]
            if offstr >= 'a' and offstr <= 'd':
                off = registers[offstr]
            else:
                off = int(offstr)
            if cond != 0:
                ip += off - 1
        elif opcode == 'cpy':
            if param >= 'a' and param <= 'd':
                src = registers[param]
            else:
                src = int(param)
            dststr = i[2]
            if dststr >= 'a' and dststr <= 'd':
                registers[dststr] = src
            else:
                # Invalid instr, skip
                pass
        else:
            assert False, f"invalid opcode {opcode} of instruction {i} (ip {ip})"
        ip += 1
        iterations += 1
        if iterations % 1000 == 0:
            print(f"iterations {iterations}, ip {ip}, registers {registers}")
    print(f"Program finished after {iterations} iterations. Registers={registers}")
    return registers['a']

def main():
    with open('../input23.txt', 'rt') as f:
        instructions = [ln.strip().split(' ') for ln in f.readlines()]
    #backup = instructions[:]
    solution_a = execute([i[:] for i in instructions], 7)
    #print(f"Solution: {solution_a}")
    #instructions = backup[:]
    solution_b = execute([i[:] for i in instructions], 12)
    print(f"Solution: {solution_b}")


if __name__=='__main__':
    main()
