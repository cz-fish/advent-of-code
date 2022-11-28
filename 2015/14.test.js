const { expect } = require("@jest/globals");
const d14 = require("./14.js");

const input = `Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.`;

test('part1 test example', () => {
    expect(d14.part1(input, 1000)).toBe(1120);
});

test('part2 test example', () => {
    expect(d14.part2(input, 1000)).toBe(689);
});
