use std::fs::File;
use std::io::Read;
use regex::Regex;
use std::collections::BinaryHeap;
use std::collections::HashSet;

struct GridNode {
    size: u32,
    used: u32,
}

fn parse_input(text: &str) -> (Vec<GridNode>, u32, u32) {
    let mut nodes: Vec<GridNode> = vec![];
    let mut max_x = 0;
    let mut max_y = 0;

    let mut prev_x = 0;
    let mut prev_y = 0;
    
    let node_regex = Regex::new(r"node-x(\d+)-y(\d+)\W+(\d+)T\W+(\d+)T\W+(\d+)T").unwrap();

    for line in text.lines() {
        if !line.starts_with("/dev/grid") {
            continue;
        }
        let parts = node_regex.captures(line).unwrap();
        let x = parts.get(1).unwrap().as_str().parse::<u32>().unwrap();
        let y = parts.get(2).unwrap().as_str().parse::<u32>().unwrap();
        let size = parts.get(3).unwrap().as_str().parse::<u32>().unwrap();
        let used = parts.get(4).unwrap().as_str().parse::<u32>().unwrap();
        let avail = parts.get(5).unwrap().as_str().parse::<u32>().unwrap();
        // verify that the data is correct
        assert_eq!(size - used, avail);
        // verify that nodes are presented in top to bottom, left to right order
        // because we check the order here, we don't have to keep the x and y coordinates of nodes around
        assert!(
            (x == 0 && y == 0) || (x == prev_x + 1 && y == 0) || (x == prev_x && y == prev_y + 1),
            "x {} y {} prev_x {} prev_y {}", x, y, prev_x, prev_y
        );
        nodes.push(GridNode{size: size, used: used});
        if x > max_x {
            max_x = x;
        }
        if y > max_y {
            max_y = y;
        }
        prev_x = x;
        prev_y = y;
    }
    println!("max X {}, max Y {}", max_x, max_y);
    assert_eq!(nodes.len() as u32, (max_x + 1) * (max_y + 1));
    (nodes, max_x, max_y)
}

fn classify_nodes(nodes: &Vec<GridNode>) -> Vec<char> {
    let mut small_smallest_size: u32 = 0;
    let mut large_most_free: u32 = 0;
    let mut small_most_free: u32 = 0;
    let mut small_most_used: u32 = 0;
    let mut small_least_used: u32 = 0;
    let mut empty_size: u32 = 0;
    for node in nodes {
        if node.used == 0 {
            assert_eq!(empty_size, 0, "More than one empty node!");
            empty_size = node.size;
            continue;
        }
        // Assuming that all smaller nodes are < 100T, and all larger ones are > 100T
        if node.size < 100 {
            if small_smallest_size == 0 || node.size < small_smallest_size {
                small_smallest_size = node.size;
            }
            if node.size - node.used > small_most_free {
                small_most_free = node.size - node.used;
            }
            if node.used > small_most_used {
                small_most_used = node.used;
            }
            if small_least_used == 0 || node.used < small_least_used {
                small_least_used = node.used;
            }
        } else {
            if node.size - node.used > large_most_free {
                large_most_free = node.size - node.used;
            }
        }
    }
    // No small will fit into another small without moving
    assert!(small_least_used > small_most_free, "small_least_used {} > small_most_free {}", small_least_used, small_most_free);
    // No small will fit into any large
    assert!(large_most_free < small_smallest_size, "largest_most_free {} < small_smallest_size {}", large_most_free, small_smallest_size);
    // Any small will fit into any other small if the target is free
    assert!(small_most_used <= small_smallest_size, "small_most_used {} <= small_smallest_size {}", small_most_used, small_smallest_size);
    // Any small will fit into the empty node
    assert!(empty_size >= small_most_used, "empty_size {} >= small_most_used {}", empty_size, small_most_used);
    
    println!("Assertions passed");

    nodes.iter().map(|node| match node {
        n if n.used == 0 => {'_'},
        n if n.size < 100 => {'.'},
        _ => {'#'}
    }).collect()
}

fn count_movable_pairs(nodes: &Vec<GridNode>) -> u32 {
    let mut result: u32 = 0;
    for first_index in 0 .. nodes.len() {
        let first = &nodes[first_index];
        let first_size = first.used;
        if first_size == 0 {
            continue;
        }
        for second_index in 0 .. nodes.len() {
            let second = &nodes[second_index];
            if first_index != second_index && second.used + first_size <= second.size {
                result += 1;
            }
        }
    }
    result
}

fn find_empty_node(grid: &Vec<char>, max_y: u32) -> (u32, u32) {
    let pos = grid.iter().position(|x| *x == '_').unwrap() as u32;
    (pos / max_y, pos % max_y)
}

fn calculate_cost(moves: u32, space: (u32, u32), goal: (u32, u32)) -> i32 {
    let sx = space.0 as i32;
    let sy = space.1 as i32;
    let gx = goal.0 as i32;
    let gy = goal.1 as i32;
    let dist = (sx + sy) + (gx - sx).abs() + (gy - sy).abs();
    dist + moves as i32
}

static MOVES: [(i32, i32); 4] = [(-1, 0), (1, 0), (0, -1), (0, 1)];

fn count_moves(nodes: &Vec<GridNode>, max_x: u32, max_y: u32) -> u32 {
    // NOTE: nodes in the grid are in column order, top to bottom, left to right
    let grid = classify_nodes(&nodes);
    // goal data is in (max_x, 0)
    // target is (0, 0)
    // there should be a '_' somewhere
    //
    // we could find shortest path from goal to target and work out _ movements around the path.
    //  - probably not guaranteed to be optimal
    // unique positions - key (_ position and G position), everything else is irrelevant, states are equal
    // A* ... man. dist. of G from target + man. dist of _ from G   + man.dist of _ from target (?? probably not)
    let height = max_y + 1;
    let original_goal = (max_x, 0 as u32);
    let original_space = find_empty_node(&grid, height);

    let mut q = BinaryHeap::new();
    q.push((-1, original_space, original_goal, 0));

    let mut known = HashSet::new();

    // iteration counter for debugging purposes
    //let mut counter = 0;

    // until a solution is found
    while q.len() > 0 {
        // take the most promising state
        let (_, space, goal, moves) = q.pop().unwrap();
        /*
        counter += 1;
        if counter % 10000 == 0 {
            println!("counter {}, Space {:?}, goal {:?}, moves {}", counter, space, goal, moves);
        }
        */
        if goal.0 == 0 && goal.1 == 0 {
            // goal is in the top left corner -> solution reached
            return moves;
        }
        // skip states that were already visited
        if known.contains(&(space, goal)) {
            continue;
        }
        known.insert((space, goal));
        // convert space index to x,y coordinate pair
        // for 4 possible moves of the space
        for dir in 0 .. 4 {
            let nx = space.0 as i32 + MOVES[dir].0;
            let ny = space.1 as i32 + MOVES[dir].1;
            if nx < 0 || ny < 0 || nx > max_x as i32 || ny > max_y as i32 {
                // move out of bounds
                continue;
            }
            let nspace = (nx as u32, ny as u32);
            if grid[(nspace.0 * height + nspace.1) as usize] == '#' {
                // move from a stationery node that is too big to move
                continue;
            }
            // move is allowed
            // if the target node is our goal data node, move it
            let ngoal = match nspace == goal { true => space, _ => goal };
            let cost = calculate_cost(moves, nspace, ngoal);
            q.push((-cost, nspace, ngoal, moves + 1));
        }
    }
    panic!("Solution not found");
}

fn main() {
    let mut file = File::open("input22.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let (nodes, max_x, max_y) = parse_input(&text);
    println!("Part 1: {}", count_movable_pairs(&nodes));
    println!("Part 2: {}", count_moves(&nodes, max_x, max_y));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_line_parsing() {
        let sample_text = "root@ebhq-gridcenter# df -h\n\
            Filesystem              Size  Used  Avail  Use%\n\
            /dev/grid/node-x0-y0     87T   71T    16T   81%\n\
            /dev/grid/node-x0-y1     93T   72T    21T   77%\n";
        let (nodes, max_x, max_y) = parse_input(&sample_text);
        assert_eq!(nodes.len(), 2);
        assert_eq!(max_x, 0);
        assert_eq!(max_y, 1);
        let first = &nodes[0];
        assert_eq!(first.size, 87);
        assert_eq!(first.used, 71);
        let second = &nodes[1];
        assert_eq!(second.size, 93);
        assert_eq!(second.used, 72);
    }

    #[test]
    fn test_moving_pairs() {
        let nodes = vec![
            GridNode{size: 100, used: 30}, // A
            GridNode{size: 30, used: 0},   // B
            GridNode{size: 20, used: 20},  // C
        ];
        // A to B, C to A, C to B => 3 pairs
        assert_eq!(count_movable_pairs(&nodes), 3);
    }

    #[test]
    fn test_classify_nodes() {
        let mut nodes: Vec<GridNode> = vec![];
        nodes.push(GridNode{size: 86, used: 44});
        nodes.push(GridNode{size: 92, used: 0});
        nodes.push(GridNode{size: 532, used: 528});
        nodes.push(GridNode{size: 70, used: 66});
        let expected: Vec<char> = vec!['.', '_', '#', '.'];
        assert_eq!(classify_nodes(&nodes), expected);
    }

    #[test]
    fn test_find_empty_node() {
        // The grid is in column-major order
        let grid = vec!['.', '#', '.', '.', '_', '#', '.', '.', '.', '#' , '#', '#'];
        // grid has 12 nodes, space is at position 4
        // if the grid is 4x3, the space position is (1, 1)
        assert_eq!(find_empty_node(&grid, 3), (1, 1));
        // if the grid is 2x6, the space position is (0, 4)
        assert_eq!(find_empty_node(&grid, 6), (0, 4));
        // if the grid is 3x4, the space position is (1, 0)
        assert_eq!(find_empty_node(&grid, 4), (1, 0));
        // if the grid is 6x2, the space position is (2, 0)
        assert_eq!(find_empty_node(&grid, 2), (2, 0));
    }

    #[test]
    fn test_find_empty_node_in_given_example() {
        // 3x3, space right in the middle
        let grid = vec!['.', '.', '#', '.', '_', '.', '.', '.', '.'];
        assert_eq!(find_empty_node(&grid, 3), (1, 1));
    }

    #[test]
    fn test_part2() {
        let input = "Filesystem            Size  Used  Avail  Use%\n\
            /dev/grid/node-x0-y0   10T    8T     2T   80%\n\
            /dev/grid/node-x0-y1   11T    6T     5T   54%\n\
            /dev/grid/node-x0-y2   320T   316T     4T   87%\n\
            /dev/grid/node-x1-y0    9T    7T     2T   77%\n\
            /dev/grid/node-x1-y1    8T    0T     8T    0%\n\
            /dev/grid/node-x1-y2   11T    7T     4T   63%\n\
            /dev/grid/node-x2-y0   10T    6T     4T   60%\n\
            /dev/grid/node-x2-y1    9T    8T     1T   88%\n\
            /dev/grid/node-x2-y2    9T    6T     3T   66%\n";
        let (nodes, max_x, max_y) = parse_input(&input);
        assert_eq!(max_x, 2);
        assert_eq!(max_y, 2);
        assert_eq!(nodes.len(), 9);
        assert_eq!(count_moves(&nodes, max_x, max_y), 7);
    }
}
