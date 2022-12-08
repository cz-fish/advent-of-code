const { expect } = require("@jest/globals");
const d08 = require("./08.js");

test('part1 test example', () => {
    expect(d08.part1(`30373\n25512\n65332\n33549\n35390\n`)).toBe(21);
});


test('part2 test example', () => {
    expect(d08.part2(`30373\n25512\n65332\n33549\n35390\n`)).toBe(8);
});

