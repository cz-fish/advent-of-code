use std::fs::File;
use std::io::Read;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;

type Grid = Vec<Vec<char>>;
type DistMat = HashMap<char, HashMap<char, usize>>;

fn parse_grid(text: &str) -> Grid {
    let mut grid: Grid = vec![];
    for line in text.lines() {
        grid.push(line.chars().collect::<Vec<char>>());
    }
    grid
}

fn find_all_locations(grid: &Grid) -> HashMap<char, (usize, usize)> {
    let mut points = HashMap::new();
    for row in 0 .. grid.len() {
        for col in 0 .. grid[row].len() {
            let ch = grid[row][col];
            if ch >= '0' && ch <= '9' {
                points.insert(ch, (row, col));
            }
        }
    }
    points
}

fn bfs_distances_from(grid: &Grid, from: char, start: &(usize, usize)) -> HashMap<char, usize> {
    let mut dists = HashMap::new();
    let mut visited: HashSet<(usize, usize)> = HashSet::new();
    let mut q = VecDeque::new();
    q.push_back((start.0, start.1, 0));
    visited.insert(*start);
    while !q.is_empty() {
        let (row, col, dist) = q.pop_front().unwrap();
        let c = grid[row][col];
        if c >= '0' && c <= '9' && c != from {
            assert!(!dists.contains_key(&c));
            dists.insert(c, dist);
            // TODO: can break early if all numbers discovered
        }
        for (dr, dc) in [(0, -1), (0, 1), (-1, 0), (1, 0)] {
            // We know that there is a border around the map, so we can't get to negative coordinates
            let nr = (row as i32 + dr) as usize;
            let nc = (col as i32 + dc) as usize;
            let pos = (nr, nc);
            if !visited.contains(&pos) && grid[nr][nc] != '#' {
                visited.insert(pos);
                q.push_back((nr, nc, dist + 1));
            }
        }
    }
    dists
}

fn make_distance_matrix(grid: &Grid) -> DistMat {
    // Find all points of interest in the grid
    let points = find_all_locations(grid);
    // Find shortest distances between each pair of points. -> Run BFS from each point
    // Create a distance matrix between the points
    // TODO: we don't need the full matrix, as it will be symmetrical. We just need half of it.
    let mut distances: DistMat = HashMap::new();
    for (pt, coords) in &points {
        distances.insert(*pt, bfs_distances_from(grid, *pt, coords));
    }

    /*
    // -- Debug only code
    let n_points = points.len() as u8;
    for f in 0 .. n_points {
        let f_char = ('0' as u8 + f) as char;
        for t in 0 .. n_points {
            if f == t {
                print!("0 ");
            } else {
                let t_char = ('0' as u8 + t) as char;
                print!("{} ", distances[&f_char][&t_char]);
            }
        }
        println!();
    }
    // --
    */

    distances
}

fn count_robot_steps(dists: &DistMat, return_to_start: bool) -> usize {
    let n_points = dists.len();
    // In the distance matrix, run Dijkstra to find the shortest overall path
    let mut q = BinaryHeap::new();
    let start = '0';
    q.push((0 as isize, start, String::from("")));
    while !q.is_empty() {
        let (mdist, pos, visited) = q.pop().unwrap();
        let dist = (-mdist) as usize;
        if (visited.len() == n_points) || (visited.len() == n_points - 1 && !return_to_start) {
            // All points visited, and returned to start (if applicable).
            // This is the shortest path
            return dist;
        } else if visited.len() == n_points - 1 {
            // All points visited, but not returned to start yet
            let dist_to_start = dists[&pos][&start];
            let mut new_visited = visited.clone();
            new_visited.push(start);
            let ndist = -((dist + dist_to_start) as isize);
            q.push((ndist, start, new_visited));
        } else {
            // Try all other non-visited nodes
            for next_i in 1 .. n_points {
                let next_c = ('0' as u8 + next_i as u8) as char;
                if visited.contains(next_c) {
                    continue;
                }
                let dist_to_next = dists[&pos][&next_c];
                let mut new_visited = visited.clone();
                new_visited.push(next_c);
                let ndist = -((dist + dist_to_next) as isize);
                q.push((ndist, next_c, new_visited));
            }
        }
    }
    panic!("Solution not found");
}

fn main() {
    let mut file = File::open("input24.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let grid = parse_grid(&text);
    let distances = make_distance_matrix(&grid);
    println!("Part 1: {}", count_robot_steps(&distances, false));
    println!("Part 2: {}", count_robot_steps(&distances, true));
}
