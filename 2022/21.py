#!/usr/bin/python3.8

from aoc import Env

e = Env(21)
e.T("""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""", 152, 301)


def make_monkey_list(input):
    monkeys = {}
    for ln in input.get_valid_lines():
        parts = ln.split(' ')
        assert len(parts) == 2 or len(parts) == 4
        monkey = parts[0][:4]
        assert monkey not in monkeys, f"Monkey '{monkey}' redefined"
        if len(parts) == 2:
            monkeys[monkey] = int(parts[1])
        else:
            assert len(parts[1]) == 4 and len(parts[3]) == 4, ln
            assert parts[2] in '+-*/'
            monkeys[monkey] = [parts[2], parts[1], parts[3], None]
    print(f"{len(monkeys)} monkeys")
    return monkeys


def apply_op(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a // b
    else:
        assert False


def evaluate(monkeys, which):
    monkey = monkeys[which]
    if type(monkey) == int:
        return monkey
    op, left, right, val = monkey
    if val is not None:
        return val
    a = evaluate(monkeys, left)
    b = evaluate(monkeys, right)
    val = apply_op(a, b, op)
    monkey[3] = val
    return val


def part1(input):
    monkeys = make_monkey_list(input)
    assert 'root' in monkeys
    return evaluate(monkeys, 'root')


e.run_tests(1, part1)
e.run_main(1, part1)


def left_inverse(op, target, v):
    if op == '+':
        # target = X + v
        # X = target - v
        return target - v
    elif op == '-':
        return target + v
    elif op == '*':
        x = target // v
        assert x * v == target
        return x
    elif op == '/':
        return target * v
    assert False, op


def right_inverse(op, target, v):
    if op == '+':
        # target = v + X
        # X = target - v
        return target - v
    elif op == '-':
        # target = v - X
        # X + target = v
        # X = v - target
        return v - target
    elif op == '*':
        # target = v * X
        # X = target // v
        x = target // v
        assert v * x == target
        return x
    elif op == '/':
        # target = v / X
        # X * target = v
        # X = v // target
        assert target != 0
        x = v // target
        assert x != 0
        assert x * target == v
        return x
    assert False, op


class MonkeyNode:
    def __init__(self, is_root, is_human, name, value):
        self.is_root = is_root
        self.is_human = is_human
        self.name = name
        self.value = value
        self.op = None
        self.parent = None
        self.left = None
        self.right = None
        self.has_human_subtree = False

    def evaluate_non_human(self):
        if self.is_human:
            self.has_human_subtree = True
            return None
        if self.value is not None:
            return self.value
        v1 = self.left.evaluate_non_human()
        v2 = self.right.evaluate_non_human()
        if v1 is None or v2 is None:
            self.has_human_subtree = True
            return None
        self.value = apply_op(v1, v2, self.op)
        return self.value

    def pass_down(self, target):
        if self.is_human:
            self.value = target
            return self.value
        assert self.has_human_subtree
        if self.left.has_human_subtree:
            right = self.right.value
            v = self.left.pass_down(left_inverse(self.op, target, right))
            self.value = apply_op(v, right, self.op)
        elif self.right.has_human_subtree:
            left = self.left.value
            v = self.right.pass_down(right_inverse(self.op, target, left))
            self.value = apply_op(left, v, self.op)
        return self.value
    
    def print(self, indent):
        i = ' ' * indent
        print(f"{i}[\"{self.name}\" {'R' if self.is_root else 'H' if self.is_human else ''} {self.value} {self.op}]")
        if self.left is not None:
            self.left.print(indent + 2)
            self.right.print(indent + 2)


def make_monkey_tree(monkey_list):
    nodes = {}
    root_node = None
    human_node = None
    # Make all tree nodes
    for name, prop in monkey_list.items():
        is_root = (name == 'root')
        is_human = (name == 'humn')
        if type(prop) == int:
            value = prop
        else:
            value = None
        node = MonkeyNode(is_root, is_human, name, value)
        nodes[name] = node
        if is_root:
            root_node = node
        if is_human:
            human_node = node
    # Plug all child references
    for name, prop in monkey_list.items():
        node = nodes[name]
        if type(prop) == list:
            node.op = prop[0]
            node.left = nodes[prop[1]]
            node.right = nodes[prop[2]]
            assert node.left.parent is None
            node.left.parent = node
            assert node.right.parent is None
            node.right.parent = node
    return root_node, human_node


def calculate_known_subtree(root):
    assert root is not None and root.left is not None and root.right is not None
    v1 = root.left.evaluate_non_human()
    v2 = root.right.evaluate_non_human()
    assert (v1 is None and v2 is not None) or (v1 is not None and v2 is None)
    if v1 is None:
        return v2, root.left
    if v2 is None:
        return v1, root.right


def part2(input):
    monkeys = make_monkey_list(input)
    root, human = make_monkey_tree(monkeys)
    target, human_subtree = calculate_known_subtree(root)
    print(f"Target value: {target}")
    human_subtree.pass_down(target)
    # root.print(0)
    return human.value


e.run_tests(2, part2)
e.run_main(2, part2)
