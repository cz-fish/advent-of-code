#!/usr/bin/python3.8

from pyaoc import Env

e = Env(18)
e.T("[[1,2],[[3,4],5]]", 143, None)
e.T("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384, None)
e.T("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445, None)
e.T("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791, None)
e.T("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137, None)
e.T("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488, None)
e.T("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""", 4140, 3993)


class Number():
    def __init__(self, left, right):
        if isinstance(left, Number):
            left.parent = self
        self.left = left
        if isinstance(right, Number):
            right.parent = self
        self.right = right
        self.parent = None

    @classmethod
    def _parse_one(cls, line, i):
        num = None
        while i < len(line):
            c = line[i]
            if c == '[':
                assert num is None
                return Number.parse(line, i)
            elif c in '],':
                assert num is not None
                return num, i
            elif c >= '0' and c <= '9':
                if num is None:
                    num = 0
                num = 10 * num + ord(c) - ord('0')
                i += 1
            else:
                assert False
        else:
            assert False

    @classmethod
    def parse(cls, line, i = 0):
        assert line[i] == '['
        left, i = Number._parse_one(line, i + 1)
        assert line[i] == ','
        right, i = Number._parse_one(line, i + 1)
        assert line[i] == ']'
        return Number(left, right), i + 1

    def reduce(self):
        retry = True
        while retry:
            retry = self.explode()
            if retry:
                continue
            retry = self.split()

    def explode(self):
        def find_depth_4(node, depth):
            if depth == 4:
                return node
            if isinstance(node.left, Number):
                x = find_depth_4(node.left, depth + 1)
                if x:
                    return x
            if isinstance(node.right, Number):
                return find_depth_4(node.right, depth + 1)
            return None

        node = find_depth_4(self, 0)
        if not node:
            return False

        assert not isinstance(node.left, Number) and not isinstance(node.right, Number), f"explosion node not primitive: {node}"

        def add_left(val, node):
            parent = node.parent
            if parent is None:
                return
            if node is parent.left:
                add_left(val, parent)
                return
            if not isinstance(parent.left, Number):
                parent.left += val
                return
            left = parent.left
            while True:
                if not isinstance(left.right, Number):
                    left.right += val
                    return
                left = left.right

        def add_right(val, node):
            parent = node.parent
            if parent is None:
                return
            if node is parent.right:
                add_right(val, parent)
                return
            if not isinstance(parent.right, Number):
                parent.right += val
                return
            right = parent.right
            while True:
                if not isinstance(right.left, Number):
                    right.left += val
                    return
                right = right.left

        def replace_0(node):
            parent = node.parent
            assert parent is not None
            if node is parent.left:
                parent.left = 0
            else:
                parent.right = 0

        add_left(node.left, node)
        add_right(node.right, node)
        replace_0(node)
        return True

    def split(self):
        def find_big_node(node):
            if isinstance(node.left, Number):
                x, l = find_big_node(node.left)
                if x:
                    return x, l
            elif node.left > 9:
                return node, True
            if isinstance(node.right, Number):
                return find_big_node(node.right)
            elif node.right > 9:
                return node, False
            return None, False

        node, isLeft = find_big_node(self)
        if not node:
            return False

        val = node.left if isLeft else node.right
        a = val // 2
        b = val - a
        if isLeft:
            node.left = Number(a, b)
            node.left.parent = node
        else:
            node.right = Number(a, b)
            node.right.parent = node
        return True

    def magnitude(self):
        if isinstance(self.left, Number):
            lval = self.left.magnitude()
        else:
            lval = self.left
        if isinstance(self.right, Number):
            rval = self.right.magnitude()
        else:
            rval = self.right
        return 3 * lval + 2 * rval

    def __str__(self):
        return '[' + str(self.left) + ',' + str(self.right) + ']'


def part1(input):
    total = None
    for ln in input.get_valid_lines():
        num, _ = Number.parse(ln)
        if total is None:
            total = num
        else:
            total = Number(total, num)
        total.reduce()
    return total.magnitude()


def test_reduce():
    exp = {
        '[[[[[9,8],1],2],3],4]': '[[[[0,9],2],3],4]',
        '[7,[6,[5,[4,[3,2]]]]]': '[7,[6,[5,[7,0]]]]',
        '[[6,[5,[4,[3,2]]]],1]': '[[6,[5,[7,0]]],3]',
        '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]': '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
        '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
    }
    good = True
    for x, e in exp.items():
        n, _ = Number.parse(x)
        n.reduce()
        r = str(n)
        if r == e:
            print(f"Reduce test OK {x} -> {r}")
        else:
            print(f"Reduce test FAIL {x} -> {r} (expected {e})")
            good = False
    return good


assert(test_reduce())

e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    best = None
    for first in range(len(lines)):
        for second in range(len(lines)):
            if second == first:
                continue
            a, _ = Number.parse(lines[first])
            b, _ = Number.parse(lines[second])
            s = Number(a, b)
            s.reduce()
            m = s.magnitude()
            if best is None or m > best:
                best = m
    return best


e.run_tests(2, part2)
e.run_main(2, part2)
