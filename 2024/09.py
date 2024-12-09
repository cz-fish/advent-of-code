#!/usr/bin/python3.12

from pyaoc import Env

def eT(*a):
    pass

e = Env(9)
e.T("""2333133121414131402""", 1928, 2858)
e.T("172", 0 + 1 + 2, 3)
e.T("102", 0 + 1 + 2, 3)
e.T("3", 0, 0)
e.T("12101", 0 + 2 + 2, 4)
e.T("11100", 1, 1)
e.T("023", 0 + 1 + 2, 2 + 3 + 4)
e.T("05302", None, 2 + 2 + 3 + 4) #22111
e.T("04302", None, 2 + 4 + 5 + 6) #22..111
e.T("0051150", None, 1+2+3+4+10) # 111112.....
# .....211111
# 012345 .. 10 + 6 + 7 +8 + 9+ 10


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


def defrag_whole_files(line):
    file_pos = {}
    free_list = []
    taken = set()
    pos = 0
    for i, val in enumerate(line):
        size = int(val)
        if i % 2 == 0:
            # file block
            file_id = i // 2
            file_pos[file_id] = (pos, size)
        else:
            # empty block
            free_list.append((pos, size))
        pos += size
    files_to_move = list(file_pos.keys())[::-1]
    for file in files_to_move:
        pos, size = file_pos[file]
        for i in range(len(free_list)):
            if i in taken:
                continue
            fpos, fsize = free_list[i]
            if fpos > pos:
                # do not move to the right
                break
            #if fpos + fsize == pos:
            #    # special case - free block just before the file we're trying to move
            #    # allow moving the whole file to the beginning of this block
            #    fsize += size
            if fsize >= size:
                # move file
                file_pos[file] = (fpos, size)
                if (fsize == size):
                    # whole empty block taken
                    taken.add(i)
                else:
                    # empty block shortened
                    free_list[i] = (fpos + size, fsize - size)
                break
    checksum = 0
    for file_id, v in file_pos.items():
        pos, size = v
        for i in range(size):
            checksum += file_id * (pos + i)
    return checksum


def part2(input):
    lines = input.get_valid_lines()
    assert len(lines) == 1
    line = lines[0]
    return defrag_whole_files(line)


e.run_tests(2, part2)
e.run_main(2, part2)

# 8439434080946 too high
