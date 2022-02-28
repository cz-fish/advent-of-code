use std::fs::File;
use std::io::Read;
use std::collections::HashSet;

/// Given a string of characters, return true if there is any substring
/// that is an even palindrome of length 4 and the shape ABBA
/// (A and B being two different characters)
fn has_even_palindrome(chunk: &str) -> bool {
    let chars: Vec<char> = chunk.chars().collect();
    for v in 2..chars.len()-1 {
        let i = v as usize;
        if chars[i] == chars[i-1] && chars[i+1] == chars[i-2] && chars[i] != chars[i+1] {
            return true;
        }
    }
    false
}

type OddPalindrome = (char, char);

/// Return a list of all odd palindromes of length 3 of the shape ABA (A and B being
/// different characters) found in the given string. The found palindromes can overlap.
/// Each palindrome is represented as a tuple of the 2 characters - A and B (of the ABA pattern)
/// in this order.
fn get_odd_palindromes(chunk: &str) -> Vec<OddPalindrome> {
    let mut pals = Vec::<OddPalindrome>::new();
    let chars: Vec<char> = chunk.chars().collect();
    for v in 1..chars.len()-1 {
        let i = v as usize;
        if chars[i+1] == chars[i-1] && chars[i] != chars[i+1] {
            pals.push((chars[i-1], chars[i]));
        }
    }
    pals
}

/// Return true if the given string chunk contains a match for any of the palindromes in the
/// given set. The given palindromes are given as tuples of characters (A, B), and the matching
/// palindrome must be of the form BAB.
fn has_any_odd_palindrome(chunk: &str, to_find: &HashSet<OddPalindrome>) -> bool {
    to_find.iter()
           .map(|(a, b)| [*b, *a, *b].iter().collect::<String>())
           .any(|s| chunk.contains(&s))
}

/// Returns true if the given string (address) conforms to the rules for TLS address:
///   * at least one of the odd parts of the address contains an even palindrome
///   * none of the even parts of the address contains any even palindrome
fn supports_tls(addr: &str) -> bool {
    let parts = addr.split(&['[', ']'][..]).collect::<Vec<&str>>();
    let good_palindrome = (0..parts.len()).step_by(2).any(|i| has_even_palindrome(parts[i]));
    let no_bad_palindrome = (1..parts.len()).step_by(2).all(|i| !has_even_palindrome(parts[i]));
    good_palindrome && no_bad_palindrome
}

/// Returns true if the given string (address) conforms to the rules for SSL address:
///   * one of the odd parts of the address contains an odd palindrome
///   * one of the even parts of the address contains the opposite palindrome to the one
///     found in the odd part.
fn supports_ssl(addr: &str) -> bool {
    let parts = addr.split(&['[', ']'][..]).collect::<Vec<&str>>();
    let mut palindromes = HashSet::<OddPalindrome>::new();
    for chunk_id in (0..parts.len()).step_by(2) {
        for pal in get_odd_palindromes(parts[chunk_id]) {
            palindromes.insert(pal);
        }
    }
    (1..parts.len()).step_by(2).any(|i| has_any_odd_palindrome(parts[i], &palindromes))
}

fn part1(text: &str) -> usize {
    text.lines()
        .filter(|ln| supports_tls(ln))
        .count()
}

fn part2(text: &str) -> usize {
    text.lines()
        .filter(|ln| supports_ssl(ln))
        .count()
}

fn main() {
    let mut file = File::open("input07.txt").unwrap();
    let mut text = String::new();
    file.read_to_string(&mut text).unwrap();

    println!("Part 1: {}", part1(&text));
    println!("Part 2: {}", part2(&text));
}

#[test]
fn test_has_even_palindrome() {
    assert!(has_even_palindrome("abba"));
    assert!(has_even_palindrome("ioxxoj"));
    assert!(!has_even_palindrome("mnop"));
    assert!(!has_even_palindrome("aaaa"));
    assert!(!has_even_palindrome("zxcvbn"));
}

#[test]
fn test_get_odd_palindromes() {
    assert_eq!(get_odd_palindromes("aba"), vec![('a', 'b')]);
    assert_eq!(get_odd_palindromes("abab"), vec![('a', 'b'), ('b', 'a')]);
    assert_eq!(get_odd_palindromes("abc"), vec![]);
    assert_eq!(get_odd_palindromes("aaa"), vec![]);
    assert_eq!(get_odd_palindromes("abacdc"), vec![('a', 'b'), ('c', 'd')]);
    assert_eq!(get_odd_palindromes("abba"), vec![]);
}

#[test]
fn test_tls_support() {
    assert!(supports_tls("abba[mnop]qrst"));
    assert!(!supports_tls("abcd[bddb]xyyx"));
    assert!(!supports_tls("aaaa[qwer]tyui"));
    assert!(supports_tls("ioxxoj[asdfgh]zxcvbn"));
    assert!(!supports_tls("abba[mnop]qrst[bddb]xyyz"));
}

#[test]
fn test_ssl_support() {
    assert!(supports_ssl("aba[bab]xyz"));
    assert!(!supports_ssl("xyx[xyx]xyx"));
    assert!(supports_ssl("aaa[kek]eke"));
    assert!(supports_ssl("zazbz[bzb]cdb"));
}

#[test]
fn test_part1() {
    assert_eq!(part1("abba[mnop]qrst\n\
                      abcd[bddb]xyyx\n\
                      aaaa[qwer]tyui\n\
                      ioxxoj[asdfgh]zxcvbn"), 2);
}

#[test]
fn test_part2() {
    assert_eq!(part2("aba[bab]xyz\n\
                      xyx[xyx]xyx\n\
                      aaa[kek]eke\n\
                      zazbz[bzb]cdb"), 3);
}
