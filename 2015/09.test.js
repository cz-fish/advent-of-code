const { expect } = require("@jest/globals");
const d09 = require("./09.js");

const example = "London to Dublin = 464\n\London to Belfast = 518\n\Dublin to Belfast = 141";

test('shortest path example works', () => {
    expect(d09.find_best_path(example, d09.shortest)).toBe(605);
});

test('longest path example works', () => {
    expect(d09.find_best_path(example, d09.longest)).toBe(982);
});
