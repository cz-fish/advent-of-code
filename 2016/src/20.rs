use std::fs::File;
use std::io::Read;
use std::cmp;

type Interval = (u32, u32);

fn parse_intervals(text: &str) -> Vec<Interval> {
    let mut intervals: Vec<Interval> = vec![];
    for line in text.lines() {
        if line.len() < 1 {
            continue;
        }
        let dash = line.find('-').unwrap();
        let lower = line[0..dash].parse::<u32>().unwrap();
        let upper = line[dash+1 .. line.len()].parse::<u32>().unwrap();
        intervals.push((lower, upper));
    }
    intervals
}

fn merge_intervals(input: &mut Vec<Interval>) -> Vec<Interval> {
    input.sort_by(|first, second| first.partial_cmp(second).unwrap());
    let mut merged: Vec<Interval> = vec![];
    for i in input {
        match merged.last_mut() {
            Some(last) if last.1 >= i.0 -1 => {
                last.1 = cmp::max(i.1, last.1);
            },
            _ => {
                merged.push(*i);
            }
        }
    }
    merged
}

fn smallest_excluded(intervals: &Vec<Interval>, min: u32, max: u32) -> u32 {
    match intervals.first() {
        Some(first) if first.0 > min => {
            min
        },
        Some(first) if first.1 + 1 <= max => {
            first.1 + 1
        },
        _ => {
            panic!("Interval fully excluded");
        }
    }
}

fn count_all_allowed(intervals: &Vec<Interval>, min: u32, max: u32) -> u32 {
    let mut count = max - min;
    for i in intervals {
        count -= i.1 - i.0 + 1;
    }
    count + 1
}

fn part1(text: &str, min: u32, max: u32) -> u32 {
    let mut intervals = parse_intervals(text);
    let merged = merge_intervals(&mut intervals);
    smallest_excluded(&merged, min, max)
}

fn part2(text: &str, min: u32, max: u32) -> u32 {
    let mut intervals = parse_intervals(text);
    let merged = merge_intervals(&mut intervals);
    count_all_allowed(&merged, min, max)
}

fn main() {
    let mut file = File::open("input20.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", part1(&text, 0, 4294967295));
    println!("Part 2: {}", part2(&text, 0, 4294967295));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1_example() {
        assert_eq!(part1("5-8\n\
                          0-2\n\
                          4-7", 0, 9), 3);
    }

    #[test]
    fn test_part2_example() {
        assert_eq!(part2("5-8\n\
                          0-2\n\
                          4-7", 0, 9), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("0-9999\n\
                          10000-20000\n\
                          20002-20003", 0, 20003), 1);
        assert_eq!(part2("", 0, 10), 11);
        assert_eq!(part2("3-8\n\
                          4-5", 0, 9), 4);
    }
}
