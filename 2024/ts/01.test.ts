import { parse_input } from './01';

describe('test 01', () => {
    test('parse numbers from input', () => {
        const input = `3   4
4   3
2   5
1   3
3   9
3   3`;
        const [left, right] = parse_input(input);
        expect(left.length).toBe(6);
        expect(left[0]).toBe(3);
        expect(left[5]).toBe(3);
        expect(right.length).toBe(6);
        expect(right[0]).toBe(4);
        expect(right[5]).toBe(3);
    });
});
