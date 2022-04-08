use std::collections::HashMap;
use std::collections::VecDeque;
use std::fs::File;
use std::io::Read;

use regex::Regex;

trait ValueReceiver {
    fn push_value(&mut self, val: u32, queue: &mut VecDeque<Give>);
}

struct Bot {
    number: u32,
    has1: Option<u32>,
    has2: Option<u32>,
    low: GiveTarget,
    high: GiveTarget,
}

struct Output {
    value: Option<u32>,
}

#[derive(Copy, Clone)]
enum GiveTarget {
    Bot(u32),
    Output(u32),
}

struct Give {
    value: u32,
    target: GiveTarget,
}

impl ValueReceiver for Bot {
    fn push_value(&mut self, val: u32, queue: &mut VecDeque<Give>) {
        if self.has1 == None {
            self.has1 = Some(val);
        } else if self.has2 == None {
            let a = self.has1.unwrap();
            self.has1 = None;
            let lower = std::cmp::min(a, val);
            let higher = std::cmp::max(a, val);

            // part 1 requirement
            if lower == 17 && higher == 61 {
                println!("Part1: numbers {} and {} handled by bot {}", lower, higher, self.number);
            }

            queue.push_back(Give {
                value: lower,
                target: self.low,
            });
            queue.push_back(Give {
                value: higher,
                target: self.high,
            })
        } else {
            // cannot happen since when the bot has 2 items it immediately gives them both away
            panic!("Bot {}: has {}, {} and was given {}", self.number, self.has1.unwrap(), self.has2.unwrap(), val);
        }
    }
}

impl ValueReceiver for Output {
    fn push_value(&mut self, val: u32, _queue: &mut VecDeque<Give>) {
        assert!(self.value.is_none());
        self.value = Some(val);
    }
}

fn get_give_target<'t>(cap: &regex::Captures<'t>, index: usize) -> GiveTarget {
    let num = cap.get(index + 1).unwrap().as_str().parse::<u32>().unwrap();
    match cap.get(index).unwrap().as_str() {
        "bot" => GiveTarget::Bot(num),
        "output" => GiveTarget::Output(num),
        &_ => panic!("wrong target capture"),
    }
}


fn parse_instructions(text: &str) -> (HashMap<u32, Bot>, VecDeque<Give>) {
    let mut bots: HashMap<u32, Bot> = HashMap::new();
    let mut give_queue: VecDeque<Give> = VecDeque::new();

    let init_regex = Regex::new(r"^value (\d+) goes to bot (\d+)$").unwrap();
    let give_regex = Regex::new(r"^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$").unwrap();

    text.lines().into_iter().for_each(|line| {
        let init_cap = init_regex.captures(line);
        let give_cap = give_regex.captures(line);
        if init_cap.is_some() {
            let cap = init_cap.unwrap();
            let val = cap.get(1).unwrap().as_str().parse::<u32>().unwrap();
            let bot = cap.get(2).unwrap().as_str().parse::<u32>().unwrap();
            give_queue.push_back(Give {value: val, target: GiveTarget::Bot(bot)});
        } else if give_cap.is_some() {
            let cap = give_cap.unwrap();
            let bot_nr = cap.get(1).unwrap().as_str().parse::<u32>().unwrap();
            let target_low = get_give_target(&cap, 2);
            let target_high = get_give_target(&cap, 4);
            assert!(!bots.contains_key(&bot_nr), "Bot {} defined twice", bot_nr);
            let bot = Bot {
                number: bot_nr,
                has1: None,
                has2: None,
                low: target_low,
                high: target_high,
            };
            bots.insert(bot_nr, bot);
        } else {
            panic!("Input line '{}' not parsed", line);
        }
    });

    (bots, give_queue)
}

fn move_numbers(bots: &mut HashMap<u32, Bot>, give_queue: &mut VecDeque<Give>) -> HashMap<u32, Output> {
    let mut outputs = HashMap::<u32, Output>::new();
    while give_queue.len() > 0 {
        let give = give_queue.pop_front().unwrap();
        match give.target {
            GiveTarget::Bot(b) => {
                bots.get_mut(&b).unwrap().push_value(give.value, give_queue);
            },
            GiveTarget::Output(o) => {
                if !outputs.contains_key(&o) {
                    outputs.insert(o, Output {
                        value: None
                    });
                }
                outputs.get_mut(&o).unwrap().push_value(give.value, give_queue);
            }
        }
    }
    outputs
}

fn multiply_first_three(outputs: & HashMap<u32, Output>) -> u32 {
    let o0 = outputs.get(&0).unwrap().value.unwrap();
    let o1 = outputs.get(&1).unwrap().value.unwrap();
    let o2 = outputs.get(&2).unwrap().value.unwrap();
    o0 * o1 * o2
}

fn main() {
    let mut file = File::open("input10.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let (mut bots, mut give_queue) = parse_instructions(&text);
    let outputs = move_numbers(&mut bots, &mut give_queue);
    let part2 = multiply_first_three(&outputs);
    println!("Part2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str =
        "value 5 goes to bot 2\n\
        bot 2 gives low to bot 1 and high to bot 0\n\
        value 3 goes to bot 1\n\
        bot 1 gives low to output 1 and high to bot 0\n\
        bot 0 gives low to output 2 and high to output 0\n\
        value 2 goes to bot 2";

    // bot 0
    // bot 1 [3]
    // bot 2 [5, 2] -> 2 to bot 1, and 5 to bot 0
    // ----
    // bot 0 [5]
    // bot 1 [3, 2] -> 2 to out 1, and 3 to bot 0
    // ----
    // bot 0 [5, 3] -> 3 to out 2, and 5 to out 0
    // ----
    // outputs: [5, 2, 3]

    #[test]
    fn test_parsing_input() {
        let (bots, give_queue) = parse_instructions(TEST_INPUT);
        assert_eq!(bots.len(), 3);
        assert_eq!(give_queue.len(), 3);
    }

    #[test]
    fn test_assigning_output() {
        let (mut bots, mut give_queue) = parse_instructions(TEST_INPUT);
        let outputs = move_numbers(&mut bots, &mut give_queue);
        assert_eq!(outputs.len(), 3);
        assert_eq!(outputs.get(&0).unwrap().value.unwrap(), 5);
        assert_eq!(outputs.get(&1).unwrap().value.unwrap(), 2);
        assert_eq!(outputs.get(&2).unwrap().value.unwrap(), 3);
    }

    #[test]
    fn test_multiply_first_three() {
        let (mut bots, mut give_queue) = parse_instructions(TEST_INPUT);
        let outputs = move_numbers(&mut bots, &mut give_queue);
        assert_eq!(multiply_first_three(&outputs), 2*3*5);
    }
}