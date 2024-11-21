#!/usr/bin/python3.8

from pyaoc import Env

e = Env(10)
e.T("""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""", 26397, 288957)


val = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
val_auto = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}
matches = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

def get_illegal_char_value(line, autocomplete=False):
    st = []
    for c in line:
        if c in '([{<':
            st.append(c)
        elif c in ')]}>':
            if not st:
                return 0
            t = st.pop()
            if matches[c] != t:
                if not autocomplete:
                    return val[c]
                else:
                    return 0
    if not autocomplete:
        return 0
    else:
        score = 0
        while(st):
            c = st.pop()
            score = score * 5 + val_auto[c]
        return score


def part1(input):
    return sum([get_illegal_char_value(ln) for ln in input.get_valid_lines()])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    scores = [get_illegal_char_value(ln, True) for ln in input.get_valid_lines()]
    scores = [x for x in scores if x > 0]
    scores.sort()
    assert len(scores) % 2 == 1
    return scores[len(scores) // 2]


e.run_tests(2, part2)
e.run_main(2, part2)
