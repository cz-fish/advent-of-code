#!/usr/bin/python3.8

from pyaoc import Env

e = Env(5, raw_lines=True)
e.T("""    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", "CMZ", "MCD")


def make_stacks(lines):
    last = lines[-1]
    nums = [int(x) for x in last.split(' ') if x]
    count = nums[-1]
    stacks = [ [] for _ in range(count)]
    for line_nr in range(len(lines)-2, -1, -1):
        line = lines[line_nr]
        for stack_nr in range(count):
            coord = stack_nr * 4 + 1
            # Original input lines have the trailing spaces to accommodate
            # for all stacks, but we've trimmed them
            if coord < len(line):
                crate = line[stack_nr * 4 + 1]
                if crate != ' ':
                    stacks[stack_nr].append(crate)
    return stacks


def print_stacks(stacks):
    # This is an opportunity for a nicer visualization
    for i, stack in enumerate(stacks):
        print(i, stack)


def apply_instructions(stacks, instructions, move):
    for instr in instructions:
        words = instr.split(' ')
        assert len(words) == 6, f'Wrong instruction format: "{instr}"'
        count = int(words[1])
        stack_from = int(words[3]) - 1
        stack_to = int(words[5]) - 1
        assert len(stacks[stack_from]) >= count, f'Not enough crates to move {count} from {stack_from} to {stack_to}'
        move(stacks, stack_from, stack_to, count)


def top_of_stacks(stacks):
    return ''.join([s[-1] for s in stacks])


def move_one(stacks, stack_from, stack_to, count):
    for _ in range(count):
        stacks[stack_to].append(stacks[stack_from].pop())


def move_many(stacks, stack_from, stack_to, count):
    temp = []
    for _ in range(count):
        temp.append(stacks[stack_from].pop())
    for _ in range(count):
        stacks[stack_to].append(temp.pop())


def part1(input):
    groups = input.get_groups()
    assert len(groups) == 2, "Input should have 2 parts - stacks and instructions"
    stacks = make_stacks(groups[0])
    #print_stacks(stacks)
    apply_instructions(stacks, groups[1], move_one)
    return top_of_stacks(stacks)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    groups = input.get_groups()
    assert len(groups) == 2, "Input should have 2 parts - stacks and instructions"
    stacks = make_stacks(groups[0])
    #print_stacks(stacks)
    apply_instructions(stacks, groups[1], move_many)
    return top_of_stacks(stacks)


e.run_tests(2, part2)
e.run_main(2, part2)
