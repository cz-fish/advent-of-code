import { parse_input, part1, part2 } from './01';

const test_input = `3   4
4   3
2   5
1   3
3   9
3   3`;

describe('test 01', () => {
    test('parse numbers from input', () => {
        const [left, right] = parse_input(test_input);
        expect(left.length).toBe(6);
        expect(left[0]).toBe(3);
        expect(left[5]).toBe(3);
        expect(right.length).toBe(6);
        expect(right[0]).toBe(4);
        expect(right[5]).toBe(3);
    });

    test('compute part 1', () => {
        const result = part1(test_input);
        expect(result).toBe(11);
    });

    test('compute part 2', () => {
        const result = part2(test_input);
        expect(result).toBe(31);
    });
});
