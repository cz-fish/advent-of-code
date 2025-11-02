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


def dense_as_hex(dense: list[int]) -> str:
    return ''.join([("0" + hex(b)[2:])[-2:] for b in dense])


def knot_hash(input_text: str) -> list[int]:
    loop = list(range(256))
    lengths = [ord(c) for c in input_text]
    # append lengths 17, 31, 73, 47, 23
    lengths.extend([17, 31, 73, 47, 23])
    # apply hash 64 times, preserving pos and skip
    twist(loop, lengths, 64)
    # reduce to dense hash by xoring blocks of 16 numbers - first 16 numbers xord together is first char of dense hash
    dense = make_dense(loop)
    return dense


def knot_hash_hex(input_text: str) -> str:
    # print dense hash as lower case hex string
    return dense_as_hex(knot_hash(input_text))
