const { expect } = require("@jest/globals");
const d10 = require("./10.js");

test('provided examples work', () => {
    const test_cases = {
        "211": "1221",
        "1": "11",
        "11": "21",
        "21": "1211",
        "1211": "111221",
        "111221": "312211",
    };

    for (test in test_cases) {
        expect(d10.expand_n_times(test, 1)).toBe(test_cases[test]);
    }
});
