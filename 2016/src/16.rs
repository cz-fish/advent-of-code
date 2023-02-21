use std::cmp;
use ascii;

static INPUT: &str = "01111010110010011";
static PART1_LEN: usize = 272;
static PART2_LEN: usize = 35651584;

static ASCII_ZERO: ascii::AsciiChar = ascii::AsciiChar::_0;
static ASCII_ONE: ascii::AsciiChar = ascii::AsciiChar::_1;

fn dragon_curve_ascii(pattern: ascii::AsciiString, len: usize) -> ascii::AsciiString {
    assert!(pattern.len() <= len);
    let mut out: ascii::AsciiString = pattern.clone();
    if out.len() == len {
        return out;
    }
    out.push(ASCII_ZERO);
    if out.len() == len {
        return out;
    }
    let chars: Vec<ascii::AsciiChar> = pattern.chars().collect();
    let take = cmp::min(pattern.len(), len - out.len());
    for i in (pattern.len() - take .. pattern.len()).rev() {
        let next_char = chars[i];
        if next_char == ASCII_ZERO {
            out.push(ASCII_ONE);
        } else {
            out.push(ASCII_ZERO);
        }
    }
    assert!(out.len() <= len);
    if out.len() == len {
        return out;
    }
    dragon_curve_ascii(out, len)
}

fn dragon_curve(pattern: &str, len: usize) -> String {
    dragon_curve_ascii(ascii::AsciiString::from_ascii(pattern).unwrap(), len).as_str().to_string()
}

fn checksum_ascii(payload: ascii::AsciiString) -> ascii::AsciiString {
    assert!(payload.len() % 2 == 0);
    let mut out = ascii::AsciiString::new();
    let chars: &[ascii::AsciiChar] = payload.as_ref();
    for i in 0 .. payload.len() / 2 {
        let first = chars[i * 2];
        let second = chars[i * 2 + 1];
        if first == second {
            out.push(ASCII_ONE);
        } else {
            out.push(ASCII_ZERO);
        }
    }
    if out.len() % 2 == 1 {
        return out;
    }
    checksum_ascii(out)
}

fn checksum(payload: &str) -> String {
    checksum_ascii(ascii::AsciiString::from_ascii(payload).unwrap()).as_str().to_string()
}

fn main() {
    let payload = dragon_curve(INPUT, PART1_LEN);
    let part1 = checksum(&payload);
    println!("Part 1: {}", part1);
    println!("Part 2: {}", checksum(&dragon_curve(INPUT, PART2_LEN)));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dragon_curve() {
        assert_eq!(dragon_curve("1", 3), "100");
        assert_eq!(dragon_curve("0", 3), "001");
        assert_eq!(dragon_curve("11111", 11), "11111000000");
        assert_eq!(dragon_curve("111100001010", 25), "1111000010100101011110000");

        assert_eq!(dragon_curve("10000", 20), "10000011110010000111");
    }

    #[test]
    fn test_cropping_dragon_curve() {
        assert_eq!(dragon_curve("1", 1), "1");
        assert_eq!(dragon_curve("10101", 8), "10101001");
        //1 -> 1,0,0 -> 100,0,110 -> 1000110,0,...
        assert_eq!(dragon_curve("1", 8), "10001100");
    }

    #[test]
    fn test_checksum() {
        assert_eq!(checksum("110010110100"), "100");

        assert_eq!(checksum("10000011110010000111"), "01100");
    }
}
