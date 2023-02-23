use md5;
use std::collections::VecDeque;

static PART1_PASSWD: &str = "bwnlcvfs";

// Take hash of password + path taken so far and apply MD5
// Get first 4 hex characters state of 4 doors: up, down, left, right
// 0-a = locked, b-f = open

// starting pos 0,0
// destination 3,3

static DIRECTIONS: &str = "UDLR";
static STEPS: [(i32, i32); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];

fn doors_from_hash(digest: &md5::Digest) -> [bool; 4] {
    let first = digest.0[0];
    let second = digest.0[1];
    let up = first >> 4;
    let down = first & 15;
    let left = second >> 4;
    let right = second & 15;
    [up > 10, down > 10, left > 10, right > 10]
}

fn get_next_paths(pos: &(i32, i32), path: &str, passwd: &str) -> Vec<(char, (i32, i32))> {
    let digest = md5::compute(format!("{}{}", passwd, path));
    let doors = doors_from_hash(&digest);
    let mut steps = Vec::<(char, (i32, i32))>::new();
    for dir in 0 .. 4 {
        if !doors[dir] {
            continue;
        }
        let new_pos = (pos.0 + STEPS[dir].0, pos.1 + STEPS[dir].1);
        if new_pos.0 >= 0 && new_pos.0 <= 3 && new_pos.1 >= 0 && new_pos.1 <= 3 {
            steps.push((DIRECTIONS.chars().nth(dir).unwrap(), new_pos));
        }
    }
    steps
}

fn shortest_path(passwd: &str) -> Option<String> {
    let start_pos = (0, 0);
    let end_pos = (3, 3);
    let mut q = VecDeque::<((i32, i32), String)>::new();
    q.push_back((start_pos.clone(), "".to_string()));
    while q.len() > 0 {
        let (pos, path) = q.pop_front().unwrap();
        if pos == end_pos {
            return Some(path);
        }
        for (dir, next_pos) in get_next_paths(&pos, &path, &passwd) {
            q.push_back((next_pos, path.clone() + &dir.to_string()));
        }
    }
    None
}

fn longest_path(passwd: &str) -> i32 {
    let mut longest: i32 = -1;

    let start_pos = (0, 0);
    let end_pos = (3, 3);
    let mut q = VecDeque::<((i32, i32), String)>::new();
    q.push_back((start_pos.clone(), "".to_string()));
    while q.len() > 0 {
        let (pos, path) = q.pop_front().unwrap();
        if pos == end_pos {
            longest = path.len() as i32;
        } else {
            for (dir, next_pos) in get_next_paths(&pos, &path, &passwd) {
                q.push_back((next_pos, path.clone() + &dir.to_string()));
            }
        }
    }

    longest
}

fn main() {
    println!("Part 1: {}", shortest_path(PART1_PASSWD).unwrap());
    println!("Part 2: {}", longest_path(PART1_PASSWD));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_shortest_path() {
        assert_eq!(shortest_path("hijkl"), None);
        assert_eq!(shortest_path("ihgpwlah"), Some("DDRRRD".to_string()));
        assert_eq!(shortest_path("kglvqrro"), Some("DDUDRLRRUDRD".to_string()));
        assert_eq!(shortest_path("ulqzkmiv"), Some("DRURDRUDDLLDLUURRDULRLDUUDDDRR".to_string()));
    }

    #[test]
    fn test_doors_from_hash() {
        // hijkl -> ced9
        assert_eq!(doors_from_hash(&md5::compute("hijkl")), [true, true, true, false]);
        // hijklD -> f2bc
        assert_eq!(doors_from_hash(&md5::compute("hijklD")), [true, false, true, true]);
        // hijklDR -> 5745
        assert_eq!(doors_from_hash(&md5::compute("hijklDR")), [false, false, false, false]);
        // hijklDUR -> all locked
        assert_eq!(doors_from_hash(&md5::compute("hijklDUR")), [false, false, false, false]);
    }

    #[test]
    fn test_longest_path() {
        assert_eq!(longest_path("ihgpwlah"), 370);
        assert_eq!(longest_path("kglvqrro"), 492);
        assert_eq!(longest_path("ulqzkmiv"), 830);
    }
}