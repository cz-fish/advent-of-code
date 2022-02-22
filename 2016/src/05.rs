use md5;
use std::io::{self, Write};
use std::collections::HashSet;

const INPUT: &str = "reyedfim";
const LENGTH: i32 = 8;

fn get_next_pwd_char(seed: &str, counter: &mut u64) -> char {
    loop {
        let digest = format!("{:x}", md5::compute(format!("{}{}", seed, *counter)));
        *counter += 1;
        if digest.starts_with("00000") {
            println!("Found hash! counter {}, digest {}", *counter, digest);
            io::stdout().flush().unwrap();
            return digest.chars().nth(5).unwrap();
        }
        if *counter % 500000 == 0 {
            println!("counter {}, hash {}", *counter, digest);
            io::stdout().flush().unwrap();
        }
    }
}

fn get_new_pwd_char(seed: &str, counter: &mut u64, filled: &HashSet<i8>) -> (i8, char) {
    loop {
        let digest = format!("{:x}", md5::compute(format!("{}{}", seed, *counter)));
        *counter += 1;
        if digest.starts_with("00000") {
            let sixth = digest.chars().nth(5).unwrap();
            let seventh = digest.chars().nth(6).unwrap();
            if ('0'..='7').contains(&sixth) {
                let pos = (sixth as i8) - ('0' as i8);
                if !filled.contains(&pos) {
                    println!("Found hash! counter {}, digest {} -> {}, {}", *counter, digest, sixth, seventh);
                    io::stdout().flush().unwrap();
                    return (pos, seventh);
                }
            }
        }
        if *counter % 500000 == 0 {
            println!("counter {}, hash {}", *counter, digest);
            io::stdout().flush().unwrap();
        }
    }
}

fn part1(seed: &str, length: i32) -> String {
    let mut counter: u64 = 0;
    (0..length).map(|_| get_next_pwd_char(&seed, &mut counter)).collect()
}

fn part2(seed: &str, length: i32) -> String {
    let mut counter: u64 = 0;
    let mut filled = HashSet::new();
    let mut digits = vec!['_'; length as usize];
    for _ in 0..length {
        let (pos, val) = get_new_pwd_char(&seed, &mut counter, &filled);
        filled.insert(pos);
        digits[pos as usize] = val;
    }
    digits.into_iter().collect()
}

fn main() {
    println!("Part 1: {}", part1(INPUT, LENGTH));
    println!("Part 2: {}", part2(INPUT, LENGTH));
}

#[test]
fn test_hash() {
    assert_eq!(part1("abc", 8), "18f47a30");
}

#[test]
fn test_positional_hash() {
    assert_eq!(part2("abc", 8), "05ace8e3");
}
