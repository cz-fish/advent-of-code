use std::fs::File;
use std::io::Read;
use regex::Regex;
mod aoclib;
use aoclib::modular;

struct Disc {
    positions: i32,
    start: i32,
}

fn parse_input(text: &str) -> Vec<Disc> {
    let re = Regex::new(r"has (\d+) positions.*is at position (\d+)").unwrap();
    text.lines()
        .into_iter()
        .filter(|line| {line.len() > 0})
        .map(|line| {
            let cap = re.captures(line);
            let values = cap.unwrap();
            let positions = values.get(1).unwrap().as_str().parse::<i32>().unwrap();
            let start = values.get(2).unwrap().as_str().parse::<i32>().unwrap();
            Disc {positions: positions, start: start}
        })
        .collect::<Vec<Disc>>()
}

fn find_earliest_time(discs: &Vec<Disc>) -> i32 {
    /*
     x + 1 = (7 - 0) mod 7 = 0 mod 7
     x + 2 = (13 - 0) mod 13 = 0 mod 13
     x + 3 = (3 - 2) mod 3 = 1 mod 3
     ...

     x = (-1) mod 7
     x = (-2) mod 13
     x = (1 - 3) mod 3
     ...
     Chinese remainder theorem
    */
    let mut coef: Vec<(i32, i32)> = Vec::new();
    for i in 0 .. discs.len() {
        let offset = (i + 1) as i32;
        let disc = &discs[i];
        // x + offset = (disc.positions - disc.start) mod disc.positions
        // x = (disc.positions - disc.start - offset) mod disc.positions
        coef.push((disc.positions - disc.start - offset, disc.positions));
    }
    modular::chinese_remainders(&coef)
}

fn find_earliest_time_bruteforce(discs: &Vec<Disc>) -> i32 {
    // We can also just bruteforce all options until we find a solution.
    // If there is a solution, it will be between 0 and the product of all the disc sizes (positions)
    let mut time: i32 = 0;
    'outer: loop {
        for d in 0 .. discs.len() {
            if (time + d as i32 + 1 + discs[d].start) % discs[d].positions != 0 {
                time += 1;
                continue 'outer;
            }
        }
        return time;
    };
}

fn main() {
    let mut file = File::open("input15.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let mut discs = parse_input(&text);
    println!("part 1: {}", find_earliest_time(&discs));
    //println!("part 1 bruteforce: {}", find_earliest_time_bruteforce(&discs));
    discs.push(Disc {positions: 11, start: 0});
    println!("part 2: {}", find_earliest_time(&discs));
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str =
        "Disc #1 has 5 positions; at time=0, it is at position 4.\n\
        Disc #2 has 2 positions; at time=0, it is at position 1.\n";

    #[test]
    fn test_parse_input() {
        let discs = parse_input(TEST_INPUT);
        assert_eq!(discs.len(), 2);
        assert_eq!(discs[0].positions, 5);
        assert_eq!(discs[0].start, 4);
        assert_eq!(discs[1].positions, 2);
        assert_eq!(discs[1].start, 1);
    }

    #[test]
    fn test_part1() {
        let discs = vec![
            Disc {positions: 5, start: 4},
            Disc {positions: 2, start: 1},
        ];
        assert_eq!(find_earliest_time(&discs), 5);
    }
    
    #[test]
    fn test_part1_bruteforce() {
        let discs = vec![
            Disc {positions: 5, start: 4},
            Disc {positions: 2, start: 1},
        ];
        assert_eq!(find_earliest_time_bruteforce(&discs), 5);
    }
}