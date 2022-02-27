use std::collections::HashMap;
use std::fs::File;
use std::io::Read;

// Used in tests
#[allow(dead_code)]
static TEST_CASE: &str = "eedadn\n\
drvtee\n\
eandsr\n\
raavrd\n\
atevrs\n\
tsrnev\n\
sdttsa\n\
rasrtv\n\
nssdts\n\
ntnada\n\
svetve\n\
tesnvt\n\
vntsnd\n\
vrdear\n\
dvrsen\n\
enarar";

fn most_frequent_letter(counter: &HashMap<char, u32>, take_max: bool) -> char {
    if take_max {
        *counter.iter()
                .max_by(|a, b| a.1.cmp(&b.1))
                .map(|(k, _v)| k)
                .unwrap()
    } else {
        *counter.iter()
                .min_by(|a, b| a.1.cmp(&b.1))
                .map(|(k, _v)| k)
                .unwrap()
    }
}

fn frequency_based_decoding(text: &str, take_max: bool) -> String {
    let lines = text.lines();
    let size = lines.last().unwrap().len();
    let mut letter_counts: Vec<HashMap<char, u32>> = (0..size).map(|_| HashMap::new()).collect();
    for line in text.lines() {
        // println!("{}", line);
        for (i, c) in line.chars().enumerate() {
            *(letter_counts[i].entry(c).or_insert(0)) += 1;
        }
    }
    (0..size).map(|i| most_frequent_letter(&letter_counts[i], take_max)).collect()
}

fn part1(text: &str) -> String {
    frequency_based_decoding(text, true)
}

fn part2(text: &str) -> String {
    frequency_based_decoding(text, false)
}


fn main() {
    let mut file = File::open("input06.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", part1(&text));
    println!("Part 2: {}", part2(&text));
}

#[test]
fn test_part1() {
    assert_eq!(part1(TEST_CASE), "easter");
}

#[test]
fn test_part2() {
    assert_eq!(part2(TEST_CASE), "advent");
}
