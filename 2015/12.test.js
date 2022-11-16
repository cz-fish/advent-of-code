const { expect } = require("@jest/globals");
const d12 = require("./12.js");

test('part1 adds up all the numbers', () => {
    expect(d12.part1("[1,2,3]")).toBe(6);
    expect(d12.part1("{\"a\":2,\"b\":4}")).toBe(6);
    expect(d12.part1("[[[3]]]")).toBe(3);
    expect(d12.part1("{\"a\":{\"b\":4},\"c\":-1}")).toBe(3);
    expect(d12.part1("{\"a\":[-1,1]}")).toBe(0);
    expect(d12.part1("[-1,{\"a\":1}]")).toBe(0);
    expect(d12.part1("[]")).toBe(0);
    expect(d12.part1("{}")).toBe(0);
});

test('part2 excludes red', () => {
    expect(d12.part2("[1,2,3]")).toBe(6);
    expect(d12.part2("[1, {\"c\": \"red\", \"b\": 2}, 3]")).toBe(4);
    expect(d12.part2("{\"d\": \"red\", \"e\": [1,2,3,4], \"f\": 5}")).toBe(0);
    expect(d12.part2("[1, \"red\", 3]")).toBe(4);
});