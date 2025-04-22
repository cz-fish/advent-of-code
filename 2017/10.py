#!/usr/bin/python3.12

from pyaoc import Env

e = Env(10, param=256)
e.T("3, 4, 1, 5", 12, None, param=5)
e.T("", None, "a2582a3a0e66e6e86e3812dcb672a272", param=256)
e.T("AoC 2017", None, "33efeb34ea91902bb2f59c9920caa6cd", param=256)
e.T("1,2,3", None, "3efbe78a8d82f29979031a4aa0b16a9d", param=256)
e.T("1,2,4", None, "63960835bcdc130f0b66d7ff4f6a5a8e", param=256)


def twist_slow(loop, lens):
    size = len(loop)
    skip = 0
    pos = 0
    for l in lens:
        # reverse from pos, l numbers
        assert l <= size
        beg = 0
        end = min(size, pos + l)
        sub = loop[pos:end]
        if end - pos < l:
            beg = l - (end - pos)
            sub.extend(loop[:beg])
        sub = sub[::-1]
        if beg > 0:
            loop = sub[-beg:] + loop[beg:pos] + sub[:-beg]
        else:
            loop = loop[:pos] + sub + loop[end:]
        # advance pos by l plus skip size
        pos = (pos + l + skip) % size
        # increment skip size
        skip += 1
        print(loop[0])
    return loop


def twist(loop, lens, repeats=1):
    size = len(loop)
    skip = 0
    pos = 0
    for _ in range(repeats):
        for v in lens:
            assert v >= 0
            assert v <= size
            beg = pos
            end = (pos + v - 1) % size
            while v > 1: # skip if v == 0 or 1
                loop[beg], loop[end] = loop[end], loop[beg]
                beg = (beg + 1) % size
                if beg == end:
                    break
                end = (end - 1) % size
                if beg == end:
                    break
            # advance pos by v plus skip size
            pos = (pos + v + skip) % size
            # increment skip size
            skip += 1
    return loop


def part1(input):
    size = e.get_param()
    loop = list(range(size))
    lengths = input.get_all_ints()
    loop = twist(loop, lengths)
    return loop[0] * loop[1]


e.run_tests(1, part1)
e.run_main(1, part1)


def make_dense(sparse):
    assert len(sparse) == 256
    dense = []
    for i in range(0, 256, 16):
        b = 0
        for j in range(16):
            b = b ^ sparse[i + j]
        dense.append(b)
    assert len(dense) == 16
    return dense


def dense_as_hex(dense):
    return ''.join([("0" + hex(b)[2:])[-2:] for b in dense])


def part2(input):
    size = e.get_param()
    loop = list(range(size))
    # use input as ascii string
    lines = input.get_valid_lines()
    assert len(lines) <= 1
    if not lines:
        lengths = []
    else:
        payload = lines[0]
        lengths = [ord(c) for c in payload]
    # append lengths 17, 31, 73, 47, 23
    lengths.extend([17, 31, 73, 47, 23])
    # apply hash 64 times, preserving pos and skip
    twist(loop, lengths, 64)
    # reduce to dense hash by xoring blocks of 16 numbers - first 16 numbers xord together is first char of dense hash
    dense = make_dense(loop)
    # print dense hash as lower case hex string
    return dense_as_hex(dense)


e.run_tests(2, part2)
e.run_main(2, part2)
