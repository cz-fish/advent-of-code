const { expect } = require("@jest/globals");
const { TestWatcher } = require("jest");
const d14 = require("./14.js");

TestWatcher('part1 test example', () => {
    expect(d14.part1()).toBe(1);
});