import { maybe_remove_one, parse_input, part1, part2 } from './02';

const test_input = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`;

describe('test 01', () => {
    test('parse numbers from input', () => {
        const nums = parse_input(test_input);
        expect(nums.length).toBe(6);
        expect(nums[0].length).toBe(5);
        expect(nums[0][0]).toBe(7);
        expect(nums[0][4]).toBe(1);
        expect(nums[1][0]).toBe(1);
        expect(nums[5][4]).toBe(9);
    });

    test('compute part 1', () => {
        const result = part1(test_input);
        expect(result).toBe(2);
    });

    test('compute part 2', () => {
        const result = part2(test_input);
        expect(result).toBe(4);
    });

    test('remove correct value', () => {
        // already in order
        expect(maybe_remove_one([1, 2, 3])).toStrictEqual([true, undefined]);
        // remove one
        expect(maybe_remove_one([1, 2, 4, 3, 5])).toStrictEqual([true, 4]);
        // remove first
        expect(maybe_remove_one([3, 1, 2, 5])).toStrictEqual([true, 3]);
        // remove last
        expect(maybe_remove_one([8, 7, 4, 9])).toStrictEqual([true, 9]);
        // cannot be fixed
        expect(maybe_remove_one([5, 6, 1, 2, 7, 8])).toStrictEqual([false, undefined]);
    });
});
