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

fn op_swap_pos(chars: &mut Vec<char>, first: usize, second: usize) {
    let t = chars[first];
    chars[first] = chars[second];
    chars[second] = t;
}

fn op_reverse(chars: &mut Vec<char>, from: usize, to: usize) {
    let mut i = from;
    let mut j = to;
    while i < j {
        let t = chars[i];
        chars[i] = chars[j];
        chars[j] = t;
        i += 1;
        j -= 1;
    }
}

fn op_rotate_left(chars: &mut Vec<char>, amount: isize) {
    let copy = chars.clone();
    for i in 0 .. chars.len() {
        chars[i] = copy[((i as isize + copy.len() as isize + amount) as usize % copy.len())];
    }
}

fn op_move(chars: &mut Vec<char>, from: usize, to: usize) {
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

fn apply_op(op: &str, password: &str) -> String {
    let operation = parse_operation(op);
    let mut chars: Vec<char> = password.chars().collect();
    match operation {
        Operation::SwapPos((first, second)) => {
            op_swap_pos(&mut chars, first, second);
        },
        Operation::SwapLetter((from, to)) => {
            let pos1 = password.find(from).unwrap();
            let pos2 = password.find(to).unwrap();
            op_swap_pos(&mut chars, pos1, pos2);
        },
        Operation::Reverse((from, to)) => {
            op_reverse(&mut chars, from, to);
        },
        Operation::RotateLeft(amount) => {
            op_rotate_left(&mut chars, amount as isize);
        },
        Operation::RotateRight(amount) => {
            op_rotate_left(&mut chars, -(amount as isize));
        },
        Operation::RotatePos(which) => {
            let pos = password.find(which).unwrap();
            let amount = (1 + pos + if pos >= 4 {1} else {0}) % password.len();
            op_rotate_left(&mut chars, -(amount as isize));
        },
        Operation::Move((from, to)) => {
            op_move(&mut chars, from, to);
        }
    };
    chars.into_iter().collect::<String>()
}

fn apply_reverse_op(op: &str, password: &str) -> String {
    let operation = parse_operation(op);
    let mut chars: Vec<char> = password.chars().collect();
    match operation {
        Operation::SwapPos((first, second)) => {
            // same as normal swap
            op_swap_pos(&mut chars, first, second);
        },
        Operation::SwapLetter((from, to)) => {
            // same as normal swap
            let pos1 = password.find(from).unwrap();
            let pos2 = password.find(to).unwrap();
            op_swap_pos(&mut chars, pos1, pos2);
        },
        Operation::Reverse((from, to)) => {
            // same as normal reverse
            op_reverse(&mut chars, from, to);
        },
        Operation::RotateLeft(amount) => {
            // rotate right instead
            op_rotate_left(&mut chars, -(amount as isize));
        },
        Operation::RotateRight(amount) => {
            // rotate left instead
            op_rotate_left(&mut chars, amount as isize);
        },
        Operation::RotatePos(which) => {
            let current_pos = password.find(which).unwrap();
            let mut original_pos: Option<usize> = None;
            for start_pos in 0 .. password.len() {
                let dest_pos = (start_pos + 1 + start_pos + if start_pos >= 4 {1} else {0}) % password.len();
                if dest_pos == current_pos {
                    if original_pos.is_some() {
                        println!("Multiple rotations possible. Operation \"{}\", password \"{}\", one option {}, another {}",
                            op, password, original_pos.unwrap(), start_pos);
                        //panic!("Multiple rotations possible. Operation \"{}\", password \"{}\", one option {}, another {}",
                        //    op, password, original_pos.unwrap(), start_pos);
                    }
                    original_pos = Some(start_pos);
                }
            }
            if !original_pos.is_some() {
                panic!("No rotation possible. Operation \"{}\", password \"{}\"", op, password);
            }
            let distance = (current_pos + password.len() - original_pos.unwrap()) % password.len();
            op_rotate_left(&mut chars, distance as isize);
        },
        Operation::Move((from, to)) => {
            // swap the source and destination
            op_move(&mut chars, to, from);
        }
    };
    chars.into_iter().collect::<String>()
}

fn scramble(instruction_text: &str, password: &str) -> String {
    let mut output: String = password.to_string();
    for ln in instruction_text.lines() {
        if ln.len() < 1 {
            continue;
        }
        output = apply_op(ln, &output);
    }
    output
}

fn unscramble(instruction_text: &str, password: &str) -> String {
    let mut output: String = password.to_string();
    for ln in instruction_text.lines().rev() {
        if ln.len() < 1 {
            continue;
        }
        output = apply_reverse_op(ln, &output);
    }
    output
}

fn main() {
    let mut file = File::open("input21.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", scramble(&text, "abcdefgh"));
    let scrambled = "fbgdceah";
    println!("Part 2: {}", unscramble(&text, scrambled));
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_OPS: &str = "swap position 4 with position 0\n\
        swap letter d with letter b\n\
        reverse positions 0 through 4\n\
        rotate left 1 step\n\
        move position 1 to position 4\n\
        move position 3 to position 0\n\
        rotate based on position of letter b\n\
        rotate based on position of letter d";

    #[test]
    fn test_example() {
        assert_eq!(scramble(TEST_OPS, "abcde"), "decab");
    }

    #[test]
    fn test_unscramble() {
        assert_eq!(unscramble(TEST_OPS, "decab"), "abcde");
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
    
    #[test]
    fn test_reverse_operations() {
        assert_eq!(apply_reverse_op("swap position 4 with position 0", "ebcda"), "abcde");
        assert_eq!(apply_reverse_op("swap letter d with letter b", "edcba"), "ebcda");
        assert_eq!(apply_reverse_op("reverse positions 0 through 4", "abcde"), "edcba");
        assert_eq!(apply_reverse_op("rotate left 1 step", "bcdea"), "abcde");
        assert_eq!(apply_reverse_op("move position 1 to position 4", "bdeac"), "bcdea");
        assert_eq!(apply_reverse_op("move position 3 to position 0", "abdec"), "bdeac");
        assert_eq!(apply_reverse_op("rotate right 2 steps", "eabcd"), "bcdea");
        assert_eq!(apply_reverse_op("rotate based on position of letter b", "ecabd"), "abdec");
        // This is not deterministic - 'd' could have been either on position 2 or 4
        assert_eq!(apply_reverse_op("rotate based on position of letter d", "decab"), "ecabd");
        // However, it seems that all reversions are deterministic in the actual input
    }
}

