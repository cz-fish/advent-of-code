const assert = require("assert");
//const fs = require("fs");

const input = "1113222113";

const tests_part1 = {
	"211": "1221",
	"1": "11",
	"11": "21",
	"21": "1211",
	"1211": "111221",
	"111221": "312211",
};

function part1(input, iter) {
	let r = input;
	while (iter > 0) {
		r = expand_once(r);
		iter--;
	}
	return r;
}

function expand_once(s) {
	let count = 0;
	let last = null;
	let res = "";
	for (i = 0; i < s.length; i++) {
		const c = s[i];
		if (c === last) {
			count++;
		} else {
			if (count > 0) {
				res += count;
				res += last
			}
			count = 1;
			last = c;
		}
	}
	if (count > 0) {
		res += count;
		res += last;
	}
	return res;
}


// tests
for (test in tests_part1) {
	const expect = tests_part1[test];
	const res = part1(test, 1);
	console.log(`${test} -> ${res} (expected ${expect})`);
	assert.equal(res, expect);
}

// actual input
const part1_res = part1(input, 40);
////console.log(part1_res);
console.log(`Part1: ${part1_res.length}`);
const part2_res = part1(part1_res, 10);
console.log(`Part2: ${part2_res.length}`);
