const { expect } = require("@jest/globals");
const d15 = require("./15.js");

const example_input = `Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
`;

test('part1 test example', () => {
    expect(d15.part1(example_input)).toBe(62842880);
});

test('part2 test example', () => {
    expect(d15.part2(example_input)).toBe(57600000);
});
