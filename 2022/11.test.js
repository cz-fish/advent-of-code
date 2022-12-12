const { expect } = require("@jest/globals");
const d11 = require("./11.js");
const fs = require('fs');

function load_test_input() {
    return fs.readFileSync('test_input-11a.txt', 'utf8');
}

test('part1 test example', () => {
    expect(d11.part1(load_test_input())).toBe(10605);
});

test('part2 test example', () => {
    expect(d11.part2(load_test_input())).toBe(2713310158);
});

