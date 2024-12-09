#!/usr/bin/python3.12

from pyaoc import Env

def eT(*a):
    pass

e = Env(9)
e.T("""2333133121414131402""", 1928, 2858)
e.T("172", 0 + 1 + 2, None)
e.T("102", 0 + 1 + 2, None)
e.T("3", 0, None)
e.T("12101", 0 + 2 + 2, None)
e.T("11100", 1, None)
e.T("023", 0 + 1 + 2, None)


def defrag_checksum(line):
    assert len(line) > 0
    left = 0
    right = len(line) + 1
    checksum = 0
    pos = 0
    to_take = 0
    #s = ""

    def take_from_end():
        nonlocal right
        nonlocal to_take
        while to_take == 0:
            right -= 2
            if right <= left:
                return None
            to_take = int(line[right])
        file_id = right // 2
        to_take -= 1
        return file_id

    while left < len(line) and left < right:
        size = int(line[left])
        if left % 2 == 0:
            # file block
            file_id = left // 2
            for i in range(size):
                checksum += (pos + i) * file_id
                #s += str(file_id)
            pos += size
        else:
            # gap block
            for i in range(size):
                val = take_from_end()
                #print(f"pos {pos + i}, val {val}")
                if val is None:
                    break
                checksum += (pos + i) * val
                #s += str(val)
            pos += size
        left += 1
    while to_take > 0:
        file_id = right // 2
        #s += str(file_id)
        checksum += pos * file_id
        to_take -= 1
        pos += 1
    #print(s)
    return checksum


def part1(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    line = lines[0]
    return defrag_checksum(line)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
