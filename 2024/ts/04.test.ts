import {
    parse_input,
    part1,
    part2 } from './04';

const test_input = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`;

describe('test 04', () => {
    test('parse grid from input', () => {
        const grid = parse_input(test_input);
        expect(grid.length).toBe(10);
        expect(grid[0].length).toBe(10);
        expect(grid[0][0]).toBe('M');
        expect(grid[9][9]).toBe('X');
    });

    test('compute part 1', () => {
        const result = part1(test_input);
        expect(result).toBe(18);
    });

    test('compute part 2', () => {
        const result = part2(test_input);
        expect(result).toBe(9);
    });
});
