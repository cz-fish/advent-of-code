use std::fs::File;
use std::io::Read;

#[derive(Debug, PartialEq)]
enum Operation {
    SwapPos((usize, usize)),
    SwapLetter((char, char)),
    RotateLeft(usize),
    RotateRight(usize),
    RotatePos(char),
    Reverse((usize, usize)),
    Move((usize, usize)),
}

fn parse_operation(op: &str) -> Operation {
    let words: Vec<&str> = op.split(' ').collect();
    if words[0] == "swap" {
        if words[1] == "position" {
            let first = words[2].parse::<usize>().unwrap();
            let second = words[5].parse::<usize>().unwrap();
            return Operation::SwapPos((first, second));
        } else if words[1] == "letter" {
            let first = words[2].chars().nth(0).unwrap();
            let second = words[5].chars().nth(0).unwrap();
            return Operation::SwapLetter((first, second));
        } else {
            panic!("Swap instruction error: '{}'", op);
        }
    } else if words[0] == "rotate" {
        if words[1] == "left" {
            let val = words[2].parse::<usize>().unwrap();
            return Operation::RotateLeft(val);
        } else if words[1] == "right" {
            let val = words[2].parse::<usize>().unwrap();
            return Operation::RotateRight(val);
        } else if words[1] == "based" {
            let anchor = words[6].chars().nth(0).unwrap();
            return Operation::RotatePos(anchor);
        } else {
            panic!("Rotate instruction error: '{}'", op);
        }
    } else if words[0] == "reverse" {
        let first = words[2].parse::<usize>().unwrap();
        let second = words[4].parse::<usize>().unwrap();
        return Operation::Reverse((first, second));
    } else if words[0] == "move" {
        let first = words[2].parse::<usize>().unwrap();
        let second = words[5].parse::<usize>().unwrap();
        return Operation::Move((first, second));
    } else {
        panic!("Wrong operator '{}'", op);
    }
}

fn apply_op(op: &str, password: &str) -> String {
    let operation = parse_operation(op);
    let mut chars: Vec<char> = password.chars().collect();
    match operation {
        Operation::SwapPos((first, second)) => {
            let t = chars[first];
            chars[first] = chars[second];
            chars[second] = t;
        },
        Operation::SwapLetter((from, to)) => {
            let pos1 = password.find(from).unwrap();
            let pos2 = password.find(to).unwrap();
            let t = chars[pos1];
            chars[pos1] = chars[pos2];
            chars[pos2] = t;
        },
        Operation::Reverse((from, to)) => {
            let mut i = from;
            let mut j = to;
            while i < j {
                let t = chars[i];
                chars[i] = chars[j];
                chars[j] = t;
                i += 1;
                j -= 1;
            }
        },
        Operation::RotateLeft(amount) => {
            let copy = chars.clone();
            for i in 0 .. chars.len() {
                chars[i] = copy[(i + amount) % copy.len()];
            }
        },
        Operation::RotateRight(amount) => {
            let copy = chars.clone();
            for i in 0 .. chars.len() {
                chars[i] = copy[((i + copy.len() - amount) % copy.len())];
            }
        },
        Operation::RotatePos(which) => {
            let copy = chars.clone();
            let pos = password.find(which).unwrap();
            let amount = (1 + pos + if pos >= 4 {1} else {0}) % copy.len();
            for i in 0 .. chars.len() {
                chars[i] = copy[((i + copy.len() - amount) % copy.len())];
            }
        },
        Operation::Move((from, to)) => {
            let t = chars[from];
            if from < to {
                for i in from .. to {
                    chars[i] = chars[i+1];
                }
            } else {
                for i in (to+1 .. from+1).rev() {
                    chars[i] = chars[i-1];
                }
            }
            chars[to] = t;
        }
    };
    chars.into_iter().collect::<String>()
}

fn apply(instruction_text: &str, password: &str) -> String {
    let mut output: String = password.to_string();
    for ln in instruction_text.lines() {
        if ln.len() < 1 {
            continue;
        }
        output = apply_op(ln, &output);
    }
    output
}

fn main() {
    let mut file = File::open("input21.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", apply(&text, "abcdefgh"));
//    println!("Part 2: {}", part2());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let password = "abcde";
        let ops = "swap position 4 with position 0\n\
                   swap letter d with letter b\n\
                   reverse positions 0 through 4\n\
                   rotate left 1 step\n\
                   move position 1 to position 4\n\
                   move position 3 to position 0\n\
                   rotate based on position of letter b\n\
                   rotate based on position of letter d";
        assert_eq!(apply(&ops, &password), "decab");
    }

    #[test]
    fn test_parse_operation() {
        assert_eq!(parse_operation("swap position 4 with position 0"), Operation::SwapPos((4, 0)));
        assert_eq!(parse_operation("swap letter d with letter b"), Operation::SwapLetter(('d', 'b')));
        assert_eq!(parse_operation("reverse positions 0 through 4"), Operation::Reverse((0, 4)));
        assert_eq!(parse_operation("rotate left 1 step"), Operation::RotateLeft(1));
        assert_eq!(parse_operation("rotate right 2 steps"), Operation::RotateRight(2));
        assert_eq!(parse_operation("move position 1 to position 4"), Operation::Move((1, 4)));
        assert_eq!(parse_operation("rotate based on position of letter b"), Operation::RotatePos('b'));
    }

    #[test]
    fn test_operations() {
        assert_eq!(apply_op("swap position 4 with position 0", "abcde"), "ebcda");
        assert_eq!(apply_op("swap letter d with letter b", "ebcda"), "edcba");
        assert_eq!(apply_op("reverse positions 0 through 4", "edcba"), "abcde");
        assert_eq!(apply_op("rotate left 1 step", "abcde"), "bcdea");
        assert_eq!(apply_op("move position 1 to position 4", "bcdea"), "bdeac");
        assert_eq!(apply_op("move position 3 to position 0", "bdeac"), "abdec");
        assert_eq!(apply_op("rotate right 2 steps", "bcdea"), "eabcd");
        assert_eq!(apply_op("rotate based on position of letter b", "abdec"), "ecabd");
        assert_eq!(apply_op("rotate based on position of letter d", "ecabd"), "decab");
    }
}

