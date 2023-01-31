const { expect } = require("@jest/globals");
const d18 = require("./dist/18");

test('part1 test example', () => {
    expect(d18.part1(`.#.#.#
...##.
#....#
..#...
#.#..#
####..`, 4)).toEqual(4);
});

test('part2 test example', () => {
    expect(d18.part2(`.#.#.#
...##.
#....#
..#...
#.#..#
####..`, 5)).toEqual(17);
});
