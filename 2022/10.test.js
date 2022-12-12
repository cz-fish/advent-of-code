const { expect } = require("@jest/globals");
const d10 = require("./10.js");
const fs = require('fs');

function load_test_input() {
    return fs.readFileSync('test_input-10a.txt', 'utf8');
}

test('part1 test example', () => {
    expect(d10.part1(load_test_input())).toBe(13140);
});


test('part2 test example', () => {
    const expectedPattern = `##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....`;
    expect(d10.part2(load_test_input())).toBe(expectedPattern);
});

