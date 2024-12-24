#!/usr/bin/python3.12

from pyaoc import Env

e = Env(24)
e.T("""x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""", 4, None)

e.T("""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""", 2024, None)


def parse_input(input):
    g = input.get_groups()
    ins = {}
    for ln in g[0]:
        assert ': ' in ln
        left, right = ln.split(': ')
        ins[left] = int(right)
    exprs = {}
    for ln in g[1]:
        tokens = ln.split()
        assert len(tokens) == 5, f"Parse {ln} -> {tokens}"
        assert tokens[1] in ["AND", "OR", "XOR"]
        assert tokens[3] == '->'
        exprs[tokens[4]] = (tokens[0], tokens[2], tokens[1])
    return ins, exprs


def eval(exprs, ins, k):
    if k in ins:
        return ins[k]
    assert k in exprs
    left, right, op = exprs[k]
    l_val = eval(exprs, ins, left)
    r_val = eval(exprs, ins, right)
    res = 0
    if op == 'OR':
        res = l_val or r_val
    elif op == 'XOR':
        res = l_val ^ r_val
    elif op == 'AND':
        res = l_val and r_val
    ins[k] = res
    return res


def evaluate_z(exprs, ins):
    val = 0
    z_keys = sorted([k for k in exprs.keys() if k.startswith('z')], reverse=True)
    for k in z_keys:
        val = val * 2 + eval(exprs, ins, k)
    return val


def part1(input):
    ins, exprs = parse_input(input)
    return evaluate_z(exprs, ins)


e.run_tests(1, part1)
e.run_main(1, part1)


def make_dot(exprs):
    with open('24.dot', 'wt') as f:
        print("digraph day24 {", file=f)
        counter = 0
        for k, v in exprs.items():
            left, right, op = v
            print(f"    {left} -> {op}{counter}", file=f)
            print(f"    {right} -> {op}{counter}", file=f)
            print(f"    {op}{counter} -> {k}", file=f)
            counter += 1
        print("}", file=f)


def check_addition(exprs, x, y):
    ins = {}
    for i in range(45):
        x_bit = (x >> (i)) & 1
        y_bit = (y >> (i)) & 1
        ins[f'x{i:02}'] = x_bit
        ins[f'y{i:02}'] = y_bit
    sol = evaluate_z(exprs, ins)
    exp = x + y
    if sol == exp:
        print(f"Match: {x} + {y} = {sol}")
        return True
    else:
        print(f"Mismatch: {x} + {y} = {exp}; got {sol}")
        for i in range(46):
            sol_bit = (sol >> i) & 1
            exp_bit = (exp >> i) & 1
            if sol_bit != exp_bit:
                print(f"Bit {i}: expected {exp_bit} was {sol_bit}")
        return False


def swap_outputs(exprs, swap_list):
    swaps = {}
    for a, b in swap_list:
        swaps[a] = b
        swaps[b] = a
    fixed = {}
    for k, v in exprs.items():
        if k in swaps:
            fixed[swaps[k]] = v
        else:
            fixed[k] = v
    return fixed


def part2(input):
    ins, exprs = parse_input(input)
    #make_dot(exprs)
    print("Original machine:")
    check_addition(
        exprs,
        0b11111111111111111111111111111111111111111111,
        0b00000000000000000000000000000000000000000001
    )
    check_addition(
        exprs,
        0b10101010101010101010101010101010101010101010,
        0b01010101010101010101010101010101010101010101
    )

    swaps = [('hmk', 'z16'), ('fcd', 'z33'), ('z20', 'fhp'), ('rvf', 'tpc')]
    fixed = swap_outputs(exprs, swaps)

    print("Fixed machine:")
    good = True
    good = good or check_addition(
        fixed,
        0b11111111111111111111111111111111111111111111,
        0b00000000000000000000000000000000000000000001
    )
    good = good or check_addition(
        fixed,
        0b10101010101010101010101010101010101010101010,
        0b01010101010101010101010101010101010101010101
    )
    assert good, "Machine wasn't fixed"
    wires = [w[0] for w in swaps] + [w[1] for w in swaps]
    wires.sort()
    return ','.join(wires)


# e.run_tests(2, part2)
e.run_main(2, part2)

"""
Something messy around output z16
bnc is the input carry bit

x16 AND y16 is going to z16, but should be going to hmk
bnc XOR vmr is going to hmk, but should be going to z16

=> swap hmk and z16

Something around z33
fcd, z33

Around bit 20
z20 is produced from AND, not XOR like elsewhere
z20, fhp

---

good cell looks like this:

X XOR Y -> a
X AND Y -> b
carry XOR a -> Z
carry AND a -> c
b OR c -> next_carry



"""
