const assert = require("assert");

const input = "vzbxkghb";
const test_part1 = {
	"abcdefgh": "abcdffaa",
	"ghijklmn": "ghjaabcc",
};

for (test in test_part1) {
  const res = next_valid_password(test);
  const expected = test_part1[test];
  console.log(`${test} -> ${res} (expected ${expected})`);
  assert.equal(res, expected);
}

