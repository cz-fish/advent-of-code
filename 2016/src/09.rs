use std::fs::File;
use std::io::Read;

use regex::Regex;

fn get_parens(input: &str, pos: usize) -> (usize, usize, usize) {
    let re = Regex::new(r"\((\d+)x(\d+)\)").unwrap();
    let bracket = re.find_at(input, pos).unwrap().as_str();
    let cap = re.captures(bracket).unwrap();
    let size = cap.get(1).unwrap().as_str().parse::<usize>().unwrap();
    let repeats = cap.get(2).unwrap().as_str().parse::<usize>().unwrap();
    let end = pos + bracket.len();
    (size, repeats, end)
}

fn expand(input: &str) -> String {
    let chars: Vec<char> = input.chars().collect();
    let mut expanded: Vec<char> = Vec::new();
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        if c == '(' {
            let (size, repeats, end) = get_parens(input, i);
            for _repeat in 0..repeats {
                for p in 0..size {
                    expanded.push(chars[end + p]);
                }
            }
            i = end + size;
        } else {
            expanded.push(c);
            i += 1;
        }
    }
    expanded.into_iter().collect()
}

fn count_size_between(input: &str, chars: &Vec<char>, start: usize, end: usize) -> usize {
    let mut size: usize = 0;
    let mut pos: usize = start;
    while pos < end {
        if chars[pos] == '(' {
            let (take, repeats, parens_end) = get_parens(input, pos);
            size += repeats * count_size_between(input, chars, parens_end, parens_end + take);
            pos = parens_end + take;
        } else {
            size += 1;
            pos += 1;
        }
    }
    size
}

fn count_ver2(input: &str) -> usize {
    let chars: Vec<char> = input.chars().collect();
    count_size_between(input, &chars, 0, input.len())
}

fn main() {
    let mut file = File::open("input09.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    let part1_res: usize = text.lines().map(|line| expand(line).len()).sum();
    println!("Part 1: {}", part1_res);

    let part2_res: usize = text.lines().map(|line| count_ver2(line)).sum();
    println!("Part 2: {}", part2_res);
}

#[test]
fn test_part1() {
    assert_eq!(expand("ADVENT").len(), 6);
    assert_eq!(expand("A(1x5)BC").len(), 7);
    assert_eq!(expand("(3x3)XYZ").len(), 9);
    assert_eq!(expand("A(2x2)BCD(2x2)EFG").len(), 11);
    assert_eq!(expand("(6x1)(1x3)A").len(), 6);
    assert_eq!(expand("X(8x2)(3x3)ABCY").len(), 18);
}

#[test]
fn test_part2() {
    assert_eq!(count_ver2("(3x3)XYZ"), 9);
    assert_eq!(count_ver2("X(8x2)(3x3)ABCY"), 20);
    assert_eq!(count_ver2("(27x12)(20x12)(13x14)(7x10)(1x12)A"), 241920);
    assert_eq!(count_ver2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"), 445);
}
