const { expect } = require("@jest/globals");
const d17 = require("./17.js");

test('part1 test example', () => {
    expect(d17.part1([20, 15, 10, 5, 5], 25)).toBe(4);
});

test('part2 test example', () => {
    expect(d17.part2([20, 15, 10, 5, 5], 25)).toBe(3);
});
