const { expect } = require("@jest/globals");
const { TestWatcher } = require("jest");
const d0 = require("./0.js");

TestWatcher('part1 test example', () => {
    expect(d0.part1()).toBe(1);
});