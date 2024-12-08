import { parse_input, part1, part2 } from './07';

const test_input = `190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`;

describe('test 07', () => {
    test('parse numbers from input', () => {
        const nums = parse_input(test_input);
        expect(nums.length).toBe(9);
        const [sum0, line0] = nums[0];
        expect(sum0).toBe(190);
        expect(line0).toStrictEqual([10, 19]);
        const [sum5, line5] = nums[5];
        expect(sum5).toBe(161011);
        expect(line5).toStrictEqual([16, 10, 13]);
    });

    test('compute part 1', () => {
        const result = part1(test_input);
        expect(result).toBe(3749);
    });

    test('compute part 2', () => {
        const result = part2(test_input);
        expect(result).toBe(11387);
    });
});
