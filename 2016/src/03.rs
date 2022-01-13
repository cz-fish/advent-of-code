use std::fs::File;
use std::io::Read;

fn is_triangle(edges: &[i32; 3]) -> bool {
    let m = edges.iter().max().unwrap();
    edges.iter().sum::<i32>() - *m > *m
}

fn part1(maybe_triangles: &Vec<[i32; 3]>) -> usize {
    maybe_triangles.iter().filter(|&edges| is_triangle(edges)).count()
}

fn part2(maybe_triangles: &Vec<[i32; 3]>) -> usize {
    assert!(maybe_triangles.len() % 3 == 0);

    // take chunks of 3 arrays of 3 integers each, transpose each 3x3 matrix, filter the result
    maybe_triangles.chunks(3)
                   .flat_map(|c| {
                        vec![
                            [c[0][0], c[1][0], c[2][0]],
                            [c[0][1], c[1][1], c[2][1]],
                            [c[0][2], c[1][2], c[2][2]]
                        ].into_iter()
                   })
                   .filter(|&edges| is_triangle(&edges))
                   .count()
}

fn get_numbers(text: &str) -> Vec<[i32; 3]> {
    let mut res = Vec::<[i32; 3]>::new();
    for line in text.lines() {
        let mut a: [i32; 3] = [0; 3];
        for (i, num) in line.split_whitespace().enumerate() {
            a[i] = num.parse().unwrap();
        }
        res.push(a)
    }
    res
}

fn main() {
    let mut file = File::open("input03.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();
    let maybe_triangles = get_numbers(&text);
    println!("Part1 result: {}", part1(&maybe_triangles));
    println!("Part2 result: {}", part2(&maybe_triangles));
}

// --- Tests ---

#[test]
fn test_get_numbers() {
    assert_eq!(get_numbers(" 100   25 11"),
               vec![[100, 25, 11]])
}

#[test]
fn test1() {
    assert_eq!(is_triangle(&[5, 10, 25]), false);
    assert_eq!(is_triangle(&[3, 4, 5]), true);
}

#[test]
#[should_panic]
fn test2_wrong_size() {
    // Length of the vector must be divisible by 3. This is length 1 and should panic
    assert_eq!(part2(&vec![
        [1, 2, 3]
    ]), 0);
}

#[test]
fn test2() {
    // When transformed, 3-4-5 is a triangle, 5-10-25 isn't, and neither is 100-200-300
    assert_eq!(part2(&vec![
        [3, 5, 100],
        [4, 10, 200],
        [5, 25, 300]
    ]), 1);
}
