const { expect } = require("@jest/globals");
const d16 = require("./16.js");

const rightSue = {
    children: 3,
    cats: 7,
    samoyeds: 2,
    pomeranians: 3,
    akitas: 0,
    vizslas: 0,
    goldfish: 5,
    trees: 3,
    cars: 2,
    perfumes: 1,
};

test('make_aunt parses correctly', () => {
    const aunt = d16.make_aunt('Sue 13: children: 4, cars: 12, trees: 0');
    expect(aunt.num).toBe(13);
    expect(aunt.children).toBe(4);
    expect(aunt.cars).toBe(12);
    expect(aunt.trees).toBe(0);
});

test('aunt matching works for part 1', () => {
    expect(d16.same_aunt_pt1({num: 1, children: 3, goldfish: 5, cars: 3}, rightSue)).toBe(false);
    expect(d16.same_aunt_pt1({num: 1, children: 3, goldfish: 5, cars: 2}, rightSue)).toBe(true);
});

test('aunt matching works for part 2', () => {
    // cats and trees mean greater than
    // pomeranians and goldfish are fewer than
    expect(d16.same_aunt_pt2({num: 1, cats: 7, trees: 3, goldfish: 5, pomeranians: 3}, rightSue)).toBe(false);
    expect(d16.same_aunt_pt2({num: 1, cats: 8, trees: 5, goldfish: 4, pomeranians: 0}, rightSue)).toBe(true);
});
