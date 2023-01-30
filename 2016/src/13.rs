use std::collections::BinaryHeap;
use std::collections::HashSet;
use std::collections::VecDeque;

fn count_bits(mut x: i32) -> i32 {
    let mut counter = 0;
    while x > 0 {
        if x & 1 > 0 {
            counter += 1;
        }
        x /= 2;
    }
    counter
}

fn is_wall(magic: i32, pos: (i32, i32)) -> bool {
    //formula: x*x + 3*x + 2*x*y + y + y*y + MAGIC
    // -> even = empty
    // -> odd = wall
    let weight = pos.0 * pos.0 + 3 * pos.0 + 2 * pos.0 * pos.1 + pos.1 + pos.1 * pos.1 + magic;
    let bits = count_bits(weight);
    bits % 2 == 1
}

fn estimate(start: (i32, i32), dest: (i32, i32)) -> i32 {
    (start.0 - dest.0).abs() + (start.1 - dest.1).abs()
}

fn find_path_length(magic: i32, dest: (i32, i32)) -> i32 {
    // A* from position (1,1) to dest
    let mut dirs = Vec::new();
    dirs.push((0, 1));
    dirs.push((1, 0));
    dirs.push((0, -1));
    dirs.push((-1, 0));
    let mut heap = BinaryHeap::new();
    let start_pos = (1, 1);
    // Heap is max heap; we want a min heap
    heap.push((0 - estimate(start_pos, dest), 0, start_pos));
    let mut visited = HashSet::new();
    visited.insert(start_pos);
    while heap.len() > 0 {
        let (_, steps, pos) = heap.pop().unwrap();
        if pos == dest {
            return steps;
        }
        visited.insert(pos);
        for dir in &dirs {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if new_pos.0 < 0 || new_pos.1 < 0
                || visited.contains(&new_pos)
                || is_wall(magic, new_pos) {
                continue;
            }
            heap.push((-(steps + 1 + estimate(new_pos, dest)), steps + 1, new_pos));
        }
    }
    panic!("Solution not found");
}

fn count_reachable(magic: i32, max_steps: i32) -> usize {
    // BFS from start with max_steps
    let mut dirs = Vec::new();
    dirs.push((0, 1));
    dirs.push((1, 0));
    dirs.push((0, -1));
    dirs.push((-1, 0));
    let start_pos = (1, 1);
    let mut queue = VecDeque::new();
    queue.push_back((0, start_pos));
    let mut visited = HashSet::new();
    visited.insert(start_pos);
    while queue.len() > 0 {
        let (steps, pos) = queue.pop_front().unwrap();
        if steps > max_steps {
            break;
        }
        visited.insert(pos);
        for dir in &dirs {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if new_pos.0 < 0 || new_pos.1 < 0
                || visited.contains(&new_pos)
                || is_wall(magic, new_pos) {
                continue;
            }
            queue.push_back((steps + 1, new_pos));
        }
    }
    visited.len()
}

fn main() {
    let magic = 1362;
    let dest = (31, 39);
    let part1 = find_path_length(magic, dest);
    println!("Part 1, steps={}", part1);
    let part2 = count_reachable(magic, 50);
    println!("Part 2, reachable rooms={}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_MAGIC: i32 = 10;

    #[test]
    fn test_count_bits() {
        assert_eq!(count_bits(0), 0);
        assert_eq!(count_bits(1), 1);
        assert_eq!(count_bits(2), 1);
        assert_eq!(count_bits(3), 2);
        assert_eq!(count_bits(10), 2);
        assert_eq!(count_bits(127), 7);
        assert_eq!(count_bits(128), 1);
    }

    #[test]
    fn test_is_wall() {
        assert!(!is_wall(TEST_MAGIC, (0, 0)));
        assert!(!is_wall(TEST_MAGIC, (1, 1)));
        assert!(!is_wall(TEST_MAGIC, (7, 4)));
        assert!(is_wall(TEST_MAGIC, (1, 0)));
        assert!(is_wall(TEST_MAGIC, (2, 3)));

        assert!(is_wall(1362, (0, 0)));
        assert!(!is_wall(1362, (1, 1)));
        assert!(!is_wall(1362, (31, 39)));
    }

    #[test]
    fn test_estimate() {
        assert_eq!(estimate((0, 0), (0, 0)), 0);
        assert_eq!(estimate((1, 1), (5, 3)), 6);
        assert_eq!(estimate((3, 3), (2, 2)), 2);
    }

    #[test]
    fn test_part1_example() {
        let distance = find_path_length(TEST_MAGIC, (7, 4));
        assert_eq!(distance, 11);
    }

    #[test]
    fn test_count_reachable() {
        /*
            magic = 10:
              0123456789
            0 c#.####.##
            1 cc#c.#...#
            2 #cccc##...
            3 ###c#.###.
            4 .##..#..#.
            5 ..##....#.
            6 #...##.###
        */
        assert_eq!(count_reachable(TEST_MAGIC, 0), 1);
        assert_eq!(count_reachable(TEST_MAGIC, 1), 3);
        assert_eq!(count_reachable(TEST_MAGIC, 2), 5);
        assert_eq!(count_reachable(TEST_MAGIC, 3), 6);
        assert_eq!(count_reachable(TEST_MAGIC, 4), 9);
    }
}
