
//#[macro_use]
//extern crate lazy_static;

use std::cmp::Ordering;
use std::collections::HashMap;
use std::fs::File;
use std::io::Read;
use std::iter::FromIterator;

use regex::Regex;

const CHECKSUM_LENGTH: usize = 5;

#[derive(Debug)]
struct Room {
    name_toks: Vec<String>,
    sector_id: u32,
    checksum: String,
}

/// Parse full room name (the whole string with dashes, numbers and brackets) into
/// Toom struct, which separates the words, sector_id, and checksum.
fn parse_room_name(room: &str) -> Room {
//    lazy_static!{
//    static ROOM_REGEX: Regex = Regex::new(r"^([a-z-]+)-([0-9]+)\[([a-z]+)\]").unwrap();
//    }
    let room_regex = Regex::new(r"^([a-z-]+)-([0-9]+)(\[([a-z]+)\])?").unwrap();

    let cap = room_regex.captures(room).unwrap();
    let long_name = cap.get(1).unwrap().as_str();
    let sector_id = cap.get(2).unwrap().as_str().parse::<u32>().unwrap();
    let checksum = cap.get(4).map_or("", |v| v.as_str());

    Room {
        name_toks: long_name.split('-').map(|x| x.to_string()).collect::<Vec<String>>(),
        sector_id: sector_id,
        checksum: checksum.to_string(),
    }
}

/// Check if a room is a real room by calculating its checksum and
/// comparing it to the checksum that is part of the room structure.
/// # Arguments
/// * `room` - a room name parsed into the Room structure
fn is_real_room(room: &Room) -> bool {
    let mut counts: HashMap<char, i32> = HashMap::new();
    for word in &room.name_toks {
        for c in word.chars() {
            *(counts.entry(c).or_insert(0)) += 1;
        }
    }
    let checksum = get_checksum_from_counters(&counts);
    checksum == room.checksum
}

/// Given a hash map with character counts, get a checksum, which
/// is the CHECKSUM_LENGTH of the most frequent characters, with ties
/// broken alphabetically.
fn get_checksum_from_counters(counters: &HashMap<char, i32>) -> String {
    let mut sorted_counts = Vec::from_iter(counters.iter());
    sorted_counts.sort_by(|a, b| {
        if a.1 > b.1 {
            Ordering::Less
        } else if b.1 > a.1 {
            Ordering::Greater
        } else {
            a.0.cmp(&b.0)
        }
    });
    let checksum: String = sorted_counts.into_iter()
                                        .take(CHECKSUM_LENGTH)
                                        .map(|k| k.0)
                                        .collect();
    checksum
}

/// Assuming that `room` is a valid room, decrypt its name by the shift cypher.
fn decrypt_name(room: &Room) -> String {
    room.name_toks
        .iter()
        .map(|word| shift(&word, room.sector_id))
        .collect::<Vec<_>>()
        .join(" ")
}

/// Shift characters of the given word by the given amount (Caesar cipher)
fn shift(word: &str, amount: u32) -> String {
    const A_OFFSET: u32 = 'a' as u32;
    word.chars()
        .map(|c| std::char::from_u32((c as u32 - A_OFFSET + amount) % 26 + A_OFFSET).unwrap())
        .collect()
}

/// Calculate the sum of sector ids of the rooms that are not decoys
fn part1(input: &str) -> u32 {
    input.lines()
         .map(|room_name| parse_room_name(room_name))
         .filter(|room| is_real_room(room))
         .map(|room| room.sector_id)
         .sum()
}

/// Decrypts real names of the valid rooms, and returns those that have something
/// to do with North Pole
fn part2(input: &str) -> Vec<(String, Room)> {
    input.lines()
         .map(|room_name| parse_room_name(room_name))
         .filter(|room| is_real_room(room))
         .map(|room| (decrypt_name(&room), room))
         .filter(|(name, _room)| name.contains("north") || name.contains("pole"))
         .collect()
}

fn main() {
    let mut file = File::open("input04.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    println!("Part1 result: {}", part1(&text));
    let p2_results = part2(&text);
    if p2_results.len() != 1 {
        println!("Got multiple results for part2!: {:?}", p2_results);
    } else {
        println!("Part2 result: {} (room name '{}')", p2_results[0].1.sector_id, p2_results[0].0);
    }
}

#[test]
fn test_pt1() {
    assert_eq!(part1("aaaaa-bbb-z-y-x-123[abxyz]\n\
                      a-b-c-d-e-f-g-h-987[abcde]\n\
                      not-a-real-room-404[oarel]\n\
                      totally-real-room-200[decoy]"), 1514);
}

#[test]
fn test_decrypt() {
    assert_eq!(decrypt_name(&parse_room_name("qzmt-zixmtkozy-ivhz-343")), "very encrypted name");
}

#[test]
fn test_parsing_room_names() {
    let room = parse_room_name("aaaaa-bbb-z-y-x-123[abxyz]");
    assert_eq!(room.sector_id, 123);
    assert_eq!(room.checksum, "abxyz");
    assert_eq!(room.name_toks, vec!["aaaaa", "bbb", "z", "y", "x"]);
}

#[test]
fn test_is_real_room() {
    assert!(is_real_room(&parse_room_name("aaaaa-bbb-z-y-x-123[abxyz]")));
    assert!(is_real_room(&parse_room_name("a-b-c-d-e-f-g-h-987[abcde]")));
    assert!(is_real_room(&parse_room_name("not-a-real-room-404[oarel]")));
    assert!(!is_real_room(&parse_room_name("totally-real-room-200[decoy]")));
}

