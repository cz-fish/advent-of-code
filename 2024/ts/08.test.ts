import {
    find_antinodes,
    get_antenna_pairs,
    parse_input,
    part1,
    part2 } from './08';

const test_input = `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`;

const test_input2 = `..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
..........`;

const test_input3 = `T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........`;

const test_input4 = `....A.A
.......`;


describe('test 08', () => {
    test('parse grid from input', () => {
        const grid = parse_input(test_input);
        expect(grid.width).toBe(12);
        expect(grid.height).toBe(12);
        expect(grid.antennas.size).toBe(2);
        expect(grid.antennas.has('0')).toBeTruthy();
        expect(grid.antennas.has('A')).toBeTruthy();
        expect(grid.antennas.get('0')?.length).toBe(4);
        expect(grid.antennas.get('A')?.length).toBe(3);
    });

    test('get pairs of antennas', () => {
        const grid = parse_input(test_input);
        const pairs = get_antenna_pairs(grid);
        expect(pairs.length).toBe(9);
    });

    test('solve test_input2', () => {
        const grid = parse_input(test_input2);
        const nodes = find_antinodes(grid, false);
        expect(nodes.size).toBe(4);
    });

    test('solve test_input3', () => {
        const grid = parse_input(test_input3);
        const nodes_pt1 = find_antinodes(grid, false);
        expect(nodes_pt1.size).toBe(3);
        const nodes_pt2 = find_antinodes(grid, true);
        expect(nodes_pt2.size).toBe(9);
    });

    test('solve test_input4', () => {
        const grid = parse_input(test_input4);
        const nodes_pt1 = find_antinodes(grid, false);
        expect(nodes_pt1.size).toBe(1);
        const nodes_pt2 = find_antinodes(grid, true);
        expect(nodes_pt2.size).toBe(4);
    });

    test('compute part 1', () => {
        const result = part1(test_input);
        expect(result).toBe(14);
    });

    test('compute part 2', () => {
        const result = part2(test_input);
        expect(result).toBe(34);
    });
});
