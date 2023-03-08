static INPUT: u32 = 3005290;

fn last_elf_standing(n: u32) -> u32 {
    let mut carry: u32 = 0;
    let mut offset: u32 = 1;
    let mut remain: u32 = n;
    let mut winner: u32 = 0;
    let mut multiplier: u32 = 2;

    while remain > 1 {
        // If carry = 0, the offset of first removed elf is 1.
        // If carry = 1, the offset of first removed elf is 0.

        // How many elves do we remove in this round?
        let remove = (remain + carry) / 2;
        // What's the index of the last removed elf?
        let last_index_removed = offset + (remove-1) * 2;
        // Was that the last elf or the second to last?
        let tail = remain - last_index_removed - 1;

        if tail == 1 {
            // Last removed elf was second to last. In the next round,
            // we will start removing from offset 0, and we carry over 1,
            // to remove 1 extra elf.
            // Because we'll be removing from offset 0, we are removing all
            // elves whose number has 0 on that bit. That means that the
            // overall winner has to have a 1 bit in that position. So
            // we add the current multiplier to the winner's index number.
            if winner + multiplier >= n {
                // Make sure not to overflow the total number of elves.
                break;
            }
            winner += multiplier;
            offset = 0;
        } else {
            // Last removed elf was last one in the circle. The next round
            // will start with offse 1 and carry 0. We'll be removing elves
            // with bit 1 in the current position, so the winner will have
            // a 0 bit at that position. That would be winner += 0 * multiplier,
            // which is a no-op.
            offset = 1;
        }
        carry = tail;

        multiplier *= 2;
        remain -= remove;
    }
    // we've been using 0-based numbers, but the result should be 1-based
    winner + 1
}

fn last_elf_across(n: u32) -> u32 {
    // for each elf, whether they have been eliminated or not
    let mut eliminated: Vec<bool> = vec![false; n as usize];
    // index of the elf whose turn it is
    let mut turn: u32 = 0;
    // index of the elf opposite the one that's playing
    let mut opposite: u32 = n / 2;
    // number of elves between playing and opposite elf; on the left from
    // the playing elf's perspective
    let mut left: i32 = (opposite - turn - 1) as i32;
    // number of elves between playing and opposite elf; on the right from
    // the playing elf's perspective
    let mut right: i32 = (n - opposite - 1) as i32;

    let next_in_game = |mut p, elim: &Vec<bool>| {
        loop {
            p = (p + 1) % n;
            if elim[p as usize] == false {
                break;
            }
        };
        p
    };

    while turn != opposite {
        // we eliminate opposite elf and move one position clockwise.
        eliminated[opposite as usize] = true;
        opposite = next_in_game(opposite, &eliminated);
        // The number on the left is unchanged by this;
        // the number on the right is decreased by 1
        right -= 1;

        // Next, the turn moves to the next elf clockwise
        // This reduces number on the left, and increases number on the right
        turn = next_in_game(turn, &eliminated);
        left -= 1;
        right += 1;

        // Make sure that left and right are still even, or left is right - 1
        if right - left > 1 {
            opposite = next_in_game(opposite, &eliminated);
            right -= 1;
            left += 1;
        }
    }
    // The indexes are 0 based, but we want a 1-based number of the winning elf.
    turn + 1
}

fn main() {
    println!("Part 1: {}", last_elf_standing(INPUT));
    println!("Part 2: {}", last_elf_across(INPUT));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example_part1() {
        assert_eq!(last_elf_standing(3), 3);
        assert_eq!(last_elf_standing(4), 1);
        assert_eq!(last_elf_standing(5), 3);
        assert_eq!(last_elf_standing(6), 5);
        assert_eq!(last_elf_standing(13), 11);
    }

    #[test]
    fn test_example_part2() {
        assert_eq!(last_elf_across(5), 2);
    }
}
