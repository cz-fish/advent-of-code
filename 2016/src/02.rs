use std::fs::File;
use std::io::Read;

fn part1(input: &str) -> i32 {
    let mut res = 0;
    let mut pos = 5;
    for line in input.lines() {
        for c in line.chars() {
            if c == 'U' && pos >= 4 {
                pos -= 3
            } else if c == 'L' && (pos-1) % 3 > 0 {
                pos -= 1
            } else if c == 'R' && (pos-1) % 3 < 2 {
                pos += 1
            } else if c == 'D' && pos < 7 {
                pos += 3
            }
        }
        res = res * 10 + pos;
    }
    res
}

fn part2(input: &str) -> String {
    let mut res = String::new();
    let keypad = &[
        "0000000",
        "0001000",
        "0023400",
        "0567890",
        "00ABC00",
        "000D000",
        "0000000"
    ];
    let mut x = 1;
    let mut y = 3;
    for line in input.lines() {
        for c in line.chars() {
            let nx = if c == 'L' { x - 1 } else if c == 'R' { x + 1 } else { x };
            let ny = if c == 'U' { y - 1 } else if c == 'D' { y + 1 } else { y };
            if keypad[ny].chars().nth(nx).unwrap() != '0' {
                x = nx;
                y = ny;
            }
        }
        res.push(keypad[y].chars().nth(x).unwrap())
    }
    res
}

fn main() {
    let mut file = File::open("input02.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    println!("Part1 result: {}", part1(&text));
    println!("Part2 result: {}", part2(&text));
}

#[test]
fn test1() {
    assert_eq!(part1(r#"ULL
                        RRDDD
                        LURDL
                        UUUUD"#), 1985)
}

#[test]
fn test2() {
    assert_eq!(part2(r#"ULL
                        RRDDD
                        LURDL
                        UUUUD"#), "5DB3")
}
