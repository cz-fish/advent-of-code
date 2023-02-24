use std::fs::File;
use std::io::Read;
use ascii::{AsciiChar, AsciiString};

fn expand(line: &str) -> String {
    let mut res = String::new();

    // Add Dots around the input from left and from right to deal with
    // the corner cases
    let mut input = AsciiString::new();
    input.push(AsciiChar::Dot);
    input.push_str(&AsciiString::from_ascii(line).unwrap());
    input.push(AsciiChar::Dot);
    let slice = input.as_slice();

    for index in 1 .. slice.len()-1 {
        let left_trap = slice[index - 1] == AsciiChar::Caret;
        //let center_trap = slice[index] == AsciiChar::Caret;
        let right_trap = slice[index + 1] == AsciiChar::Caret;
        
        // Rules:
        //   left and center are traps, right is not -> trap
        //   center and right are traps, left is not -> trap
        //   only left is trap -> trap
        //   only right is trap -> trap
        //   else clear

        if (left_trap && !right_trap) || (!left_trap && right_trap) {
            res.push('^');
        } else {
            res.push('.');
        }
    }
    res
}

fn count_safe(first: &str, lines: u32) -> u32 {
    let mut total = 0;
    let mut current = first.to_string();
    for _i in 0 .. lines {
        total += current.chars().filter(|c| *c == '.').count();
        current = expand(&current);
    }
    total as u32
}

fn main() {
    let mut file = File::open("input18.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let line = text.lines().nth(0).unwrap();

    println!("Part 1: {}", count_safe(&line, 40));
    // There is probably some memoization potential
    // in 400000 repetitions. Not implemented yet though.
    println!("Part 2: {}", count_safe(&line, 400000));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_expand() {
        assert_eq!(expand("..^^."), ".^^^^");
        assert_eq!(expand(".^^^^"), "^^..^");
        assert_eq!(expand(".^^.^.^^^^"), "^^^...^..^");
    }

    #[test]
    fn test_example() {
        assert_eq!(count_safe(".^^.^.^^^^", 10), 38);
    }
}
