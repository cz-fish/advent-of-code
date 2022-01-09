
use std::fs::File;
use std::io::Read;

use regex::Regex;

use std::collections::HashSet;

fn get_directions(input: &str) -> Vec<(char, i32)> {
    let re = Regex::new(r"([RL])(\d+)").unwrap();
    re.captures_iter(input).map(|cap| {
        (cap.get(1).unwrap().as_str().chars().nth(0).unwrap(),
         cap.get(2).unwrap().as_str().parse::<i32>().unwrap())
    }).collect::<Vec<_>>()
}

fn follow_directions(directions: &Vec<(char, i32)>) -> (i32, i32) {
    let mut pos: (i32, i32) = (0, 0);
    let mut aim = (0, 1);

    for (dir, amount) in directions {
        aim = if *dir == 'R' {(aim.1, -aim.0)} else {(-aim.1, aim.0)};
        pos.0 += aim.0 * amount;
        pos.1 += aim.1 * amount;
    }
    return pos;
}

fn follow_with_intersections(directions: &Vec<(char, i32)>) -> (i32, i32) {
    let mut pos: (i32, i32) = (0, 0);
    let mut aim = (0, 1);

    let mut visited: HashSet<(i32, i32)> = HashSet::new();
    visited.insert(pos);

    for (dir, amount) in directions {
        aim = if *dir == 'R' {(aim.1, -aim.0)} else {(-aim.1, aim.0)};
        for _i in 0 .. *amount {
            pos.0 += aim.0;
            pos.1 += aim.1;
            if visited.contains(&pos) {
                return pos;
            }
            visited.insert(pos);
        }
    }
    panic!("No place visited twice");
}

fn part1(directions: &Vec<(char, i32)>) -> i32 {
    let endpos = follow_directions(directions);
    endpos.0.abs() + endpos.1.abs()
}

fn part2(directions: &Vec<(char, i32)>) -> i32 {
    let endpos = follow_with_intersections(directions);
    endpos.0.abs() + endpos.1.abs()
}

fn main() {
    let mut file = File::open("input01.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let directions = get_directions(&text);
    println!("Part1 result: {}", part1(&directions));
    println!("Part2 result: {}", part2(&directions));
}

// --- tests ---
// R2, L3 -> 5
// R2, R2, R2 -> 2
// R5, L5, R5, R3 -> 12

#[test]
fn test_directions() {
    assert_eq!(
        get_directions("R2, L3, R100, L15"),
        vec![
            ('R', 2),
            ('L', 3),
            ('R', 100),
            ('L', 15)
        ]
    )
}

#[test]
fn test1() {
    assert_eq!(part1(&get_directions(&"R2, L3")), 5);
}

#[test]
fn test2() {
    assert_eq!(part1(&get_directions(&"R2, R2, R2")), 2);
}

#[test]
fn test3() {
    assert_eq!(part1(&get_directions(&"R5, L5, R5, R3")), 12);
}

#[test]
fn test4() {
    assert_eq!(part2(&get_directions(&"R8, R4, R4, R8")), 4);
}