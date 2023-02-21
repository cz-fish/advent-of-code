/// Bezout's identity
/// For
///     a * m + b * n = gcd(m, n),
/// find some integers a and b that satisfy the equation.
/// There are infinitely many solutions.
/// When m, n are co-prime, gcd = 1.
pub fn bezout(m: i32, n: i32) -> (i32, i32) {
    let mut s = 0;
    let mut prev_s = 1;
    let mut t = 1;
    let mut prev_t = 0;
    let mut r = n;
    let mut prev_r = m;
    while r != 0 {
        let q = prev_r / r;
        (prev_r, r) = (r, prev_r - q * r);
        (prev_s, s) = (s, prev_s - q * s);
        (prev_t, t) = (t, prev_t - q * t);
    }
    (prev_s, prev_t)
}

/// For an integer `a` and base `n`, return multiplicative
/// inverse `a'` of `a` modulo `n`, such that
///     a * a' = 1 (mod n)
/// This is assuming that `a` and `n` are co-prime.
pub fn multiplicative_inverse(num: i32, base: i32) -> i32 {
    bezout(num, base).0
}

/// Chinese Remainder Theorem
/// Given a list of modular equations
///   x = a_1 (mod n_1)
///   x = a_2 (mod n_2)
///   ...
///   x = a_k (mod n_k)
/// Find x that satisfies all of them.
/// This is assuming that all of `n_j` are pair-wise co-prime.
/// The input parameter `coef` is a list of tuples (`a_j`, `n_j`)
/// for each equation.
pub fn chinese_remainders(coef: &Vec<(i32, i32)>) -> i32 {
    if coef.len() < 1 {
        return 0;
    }

    let mut a1 = coef[0].0 as i64;
    // First equation
    // x = a_1 (mod n_1)
    // N1 is the product of all `n` numbers folded so far
    #[allow(non_snake_case)]
    let mut N1 = coef[0].1 as i64;

    // For all remaining equations
    for i in 1 .. coef.len() {
        let a2 = coef[i].0 as i64;
        let n2 = coef[i].1 as i64;
        // Determine Bezout coefficients for the i-th equation and
        // the product of all equations before i.
        let (m1, m2) = bezout(N1 as i32, n2 as i32);
        // Chinese remainder theorem:
        // x = a1 * m2 * n2 + a2 * M1 * N1
        let mut x: i64 = a1 * m2 as i64 * n2 + a2 * m1 as i64 * N1;
        N1 *= n2;
        // There are infinitely many `x`. We want the one between
        // 0 and N1 - hence modulo (i.e. rem_euclid; % would give a remainder, which could be negative)
        x = x.rem_euclid(N1);
        // In the next iteration, x becomes the coefficient of the folded term
        a1 = x;
    }
    // The last x is the result
    a1 as i32
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bezout() {
        assert_eq!(bezout(3, 5), (2, -1));
    }

    #[test]
    fn test_multiplicative_inverse() {
        assert_eq!(multiplicative_inverse(17, 19), 9);
    }

    #[test]
    fn test_chinese_remainders() {
        /*
        x = 0 (mod 17)
        x = -2 (mod 13)
        x = -3 (mod 19)
        -> x = 3417
        */
        let coef = vec![(0, 17), (-2, 13), (-3, 19)];
        assert_eq!(chinese_remainders(&coef), 3417);
    }

}
