// test salt "abc" -> answer 22728
// actual salt "yjdafjpo"

// start from 0
// test case "abc18" produces 888, but no 88888 in next 1000
// test case "abc39" produces eee and abc816 has eeeee
// test case "abc92" produces 999 and abc200 has 99999

// only consider first triplet, but any quintet

use md5;
//use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

type IndexChar = (i32, char);

const PART2_STRETCH: i32 = 2016;

fn find_triplet(hash: &Vec<char>) -> Option<char> {
    if hash.len() < 3 {
        return None;
    }

    for i in 0 .. hash.len() - 2 {
        let current = hash[i];
        if current == hash[i+1] && current == hash[i+2] {
            return Some(current);
        }
    }
    None
}

fn find_quintets(hash: &Vec<char>) -> HashSet<char> {
    let mut ans = HashSet::<char>::new();
    if hash.len() >= 5 {
        let mut row = 1;
        let mut same = hash[0];
        for i in 1 .. hash.len() {
            if hash[i] == same {
                row += 1;
                if row == 5 {
                    ans.insert(same);
                }
            } else {
                same = hash[i];
                row = 1;
            }
        }
    }
    ans
}

fn hex_char(val: u8) -> char {
    (match val {
        x if x < 10 => ('0' as u8) + x,
        x => ('a' as u8) + x - 10
    }) as char
}

fn stretch_digest(initial: md5::Digest, loops: i32) -> md5::Digest {
    let mut work = initial;
    for _i in 0 .. loops {
        let chars = work.0.iter()
                          .flat_map(|b| [hex_char(*b >> 4) as u8, hex_char(*b & 15) as u8])
                          .collect::<Vec<u8>>();
        work = md5::compute(chars);
    }
    work
}

fn get_some_hashes(salt: &str,
                   stretch: i32,
                   from: i32,
                   to: i32,
                   triplet_queue: &mut VecDeque<IndexChar>,
                   quintet_queue: &mut VecDeque<IndexChar>)
{
    for i in from .. to {
        let initial_digest = md5::compute(format!("{}{}", salt, i));
        let digest = stretch_digest(initial_digest, stretch);
        let chars = digest.0.iter()
                            .flat_map(|b| [hex_char(*b >> 4), hex_char(*b & 15)])
                            .collect::<Vec<char>>();
        let triplet = find_triplet(&chars);
        let quintets = find_quintets(&chars);
        if triplet.is_some() {
            triplet_queue.push_back((i, triplet.unwrap()));
        }
        for ch in quintets {
            quintet_queue.push_back((i, ch));
        }
    }
}

fn is_key(val: IndexChar, quintet_queue: &VecDeque<IndexChar>) -> bool {
    for pair in quintet_queue.iter() {
        if pair.0 > val.0 + 1000 {
            break;
        }
        if pair.1 == val.1 {
            return true;
        }
    }
    false
}

fn find_nth_key(salt: &str, n: i32, stretch: i32) -> i32 {
    let mut triplet_queue = VecDeque::<IndexChar>::new();
    let mut quintet_queue = VecDeque::<IndexChar>::new();
    let mut highest_hash: i32 = 0;
    let mut keys_found: i32 = 0;
    let mut current_number: i32 = 0;

    while keys_found < n {
        // make sure we have any key candidates left. If not, get some more hashes until we do
        while triplet_queue.len() == 0 {
            get_some_hashes(salt, stretch, highest_hash, highest_hash + 100, &mut triplet_queue, &mut quintet_queue);
            highest_hash += 100;
        }
        // get the next key candidate
        let next = triplet_queue.pop_front().unwrap();
        // make sure that we have enough hashes to test the next key candidate
        if highest_hash < next.0 + 1000 {
            get_some_hashes(salt, stretch, highest_hash, next.0 + 1000, &mut triplet_queue, &mut quintet_queue);
            highest_hash = next.0 + 1000;
        }
        // expire all quintets that are below the current key candidate
        while quintet_queue.len() > 0 {
            if quintet_queue.front().unwrap().0 <= next.0 {
                quintet_queue.pop_front();
            } else {
                break;
            }
        }
        // check if the key candidate is indeed a key
        if is_key(next, &quintet_queue) {
            current_number = next.0;
            keys_found += 1;
        }
    }

    current_number
}

fn main() {
    let salt = "yjdafjpo";
    let n = 64;
    let part1 = find_nth_key(salt, n, 0);
    println!("Part 1: {}", part1);
    let part2 = find_nth_key(salt, n, PART2_STRETCH);
    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn v(s: &str) -> Vec<char> {
        s.chars().collect::<Vec<char>>()
    }

    #[test]
    fn test_triplets() {
        assert!(find_triplet(&v("")).is_none());
        assert!(find_triplet(&v("abc")).is_none());
        assert!(find_triplet(&v("aabbccddeeaa")).is_none());
        assert_eq!(find_triplet(&v("aaa")).unwrap(), 'a');
        assert_eq!(find_triplet(&v("bbaaacc")).unwrap(), 'a');
        assert_eq!(find_triplet(&v("aaabbbb")).unwrap(), 'a');
    }

    #[test]
    fn test_quintets() {
        assert_eq!(find_quintets(&v("")).len(), 0);
        assert_eq!(find_quintets(&v("aaaab")).len(), 0);
        assert_eq!(find_quintets(&v("aaaaa")), HashSet::from(['a']));
        assert_eq!(find_quintets(&v("abbbbba")), HashSet::from(['b']));
        assert_eq!(find_quintets(&v("cccccccccc")), HashSet::from(['c']));
        assert_eq!(find_quintets(&v("aaaaabccccc")), HashSet::from(['a', 'c']));
        assert_eq!(find_quintets(&v("aaaaabaaaaa")), HashSet::from(['a']));
    }

    #[test]
    fn test_hex_char() {
        assert_eq!(hex_char(0), '0');
        assert_eq!(hex_char(9), '9');
        assert_eq!(hex_char(10), 'a');
        assert_eq!(hex_char(15), 'f');
    }

    #[test]
    fn test_get_some_hashes() {
        let mut triplet_queue = VecDeque::<IndexChar>::new();
        let mut quintet_queue = VecDeque::<IndexChar>::new();
        get_some_hashes("abc", 0, 0, 100, &mut triplet_queue, &mut quintet_queue);
        let triplets = triplet_queue.into_iter().collect::<Vec<IndexChar>>();

        assert_eq!(triplets, vec![
            (18, '8'),
            (39, 'e'),
            (45, 'd'),
            (64, '5'),
            (77, 'f'),
            (79, 'a'),
            (88, 'f'),
            (91, '0'),
            (92, '9'),
        ]);
    }

    #[test]
    fn test_is_key() {
        let mut quintet_queue = VecDeque::<IndexChar>::new();
        quintet_queue.push_back((1, 'a'));
        quintet_queue.push_back((999, 'b'));
        quintet_queue.push_back((1000, 'c'));
        quintet_queue.push_back((1001, 'd'));
        assert!(is_key((0, 'a'), &quintet_queue));
        assert!(is_key((0, 'b'), &quintet_queue));
        assert!(is_key((0, 'c'), &quintet_queue));
        assert!(!is_key((0, 'd'), &quintet_queue));
        assert!(is_key((1, 'd'), &quintet_queue));
        assert!(!is_key((300, 'f'), &quintet_queue));
    }

    #[test]
    fn test_part1() {
        assert_eq!(find_nth_key("abc", 1, 0), 39);
        assert_eq!(find_nth_key("abc", 64, 0), 22728);
    }
    
    #[test]
    fn test_part2() {
        assert_eq!(find_nth_key("abc", 1, PART2_STRETCH), 10);
        // Takes probably around 10 minutes to complete
        //assert_eq!(find_nth_key("abc", 64, PART2_STRETCH), 22551);
    }
}