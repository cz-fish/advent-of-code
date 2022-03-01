use std::fs::File;
use std::io::Read;

use regex::Regex;

static K_WIDTH: usize = 50;
static K_HEIGHT: usize = 6;

fn light_up_display(input: &str, width: usize, height: usize) -> Vec<Vec<bool>> {
    let re = Regex::new(r"(rect|rotate row|rotate column) \D*(\d+)\D+(\d+)").unwrap();
    let mut display = vec![vec![false; width]; height];
    for command in input.lines() {
        let matches = re.captures(command).unwrap();
        let what = matches.get(1).unwrap().as_str();
        let x = matches.get(2).unwrap().as_str().parse::<usize>().unwrap();
        let y = matches.get(3).unwrap().as_str().parse::<usize>().unwrap();

        if what == "rect" {
            for r in 0..y {
                for c in 0..x {
                    display[r as usize][c as usize] = true;
                }
            }
        } else if what == "rotate row" {
            let line: Vec<bool> = (0..width).map(|i| (i + width - y) % width)
                                            .map(|j| display[x][j])
                                            .collect();
            for i in 0..width {
                display[x][i] = line[i];
            }
        } else if what == "rotate column" {
            let line: Vec<bool> = (0..height).map(|i| (i + height - y) % height)
                                             .map(|j| display[j][x])
                                             .collect();
            for i in 0..height {
                display[i][x] = line[i];
            }
        } else {
            panic!("Wrong command {}", command);
        }
    }
    display
}

fn count_lights(display: &Vec<Vec<bool>>) -> usize {
    let mut count: usize = 0;
    for row in display.iter() {
        count += row.iter().filter(|c| **c).count();
    }
    count
}

fn print_display(display: &Vec<Vec<bool>>) -> () {
    for row in 0..display.len() {
        let line: String = display[row].iter().map(|b| if *b {'#'} else {'.'}).collect();
        println!("{}", line);
    }
}

fn part1(input: &str, width: usize, height: usize) -> usize {
    let display = light_up_display(input, width, height);
    let res = count_lights(&display);
    print_display(&display);
    res
}

fn main() {
    let mut file = File::open("input08.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", part1(&text, K_WIDTH, K_HEIGHT));
    // println!("Part 2: {}", part2(&text));
}

#[test]
fn test_part1() {
    assert_eq!(part1("rect 3x2\n\
                      rotate column x=1 by 1\n\
                      rotate row y=0 by 4\n\
                      rotate column x=1 by 1", 7, 3), 6);
}
