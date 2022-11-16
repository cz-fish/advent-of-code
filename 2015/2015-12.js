const fs = require("fs");
const assert = require("assert");

//const useTestInput = true;
const useTestInput = false;

function recSum(elem, ignoreRed=false) {
	if (typeof elem === 'number'){
		return elem;
	} else if (typeof elem === 'string') {
		return 0;
	}
	let val = 0;
	for(let idx in elem) {
		if (ignoreRed && !Array.isArray(elem) && elem[idx] === 'red') {
		    return 0;
		}
		val += recSum(elem[idx], ignoreRed);
	}
	return val;

}

function part1(data) {
	const struct = JSON.parse(data);
	return recSum(struct);
}

function part2(data) {
	const struct = JSON.parse(data);
	return recSum(struct, true);
}

function cassert(actual, expected) {
	console.log(`${actual} =?= ${expected}`);
	assert(actual === expected);
}

if (useTestInput){
	// part1
	/*
	[1,2,3] and {"a":2,"b":4} both have a sum of 6.
   [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
   {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
   [] and {} both have a sum of 0.
   */
   cassert(part1("[1,2,3]"), 6);
   cassert(part1("{\"a\":2,\"b\":4}"), 6);
   cassert(part1("[[[3]]]"), 3);
   cassert(part1("{\"a\":{\"b\":4},\"c\":-1}"), 3);
   cassert(part1("{\"a\":[-1,1]}"), 0);
   cassert(part1("[-1,{\"a\":1}]"), 0);
   cassert(part1("[]"), 0);
   cassert(part1("{}"), 0);
   console.log("All part1 tests pass");
   
   cassert(part2("[1,2,3]"), 6);
   cassert(part2("[1, {\"c\": \"red\", \"b\": 2}, 3]"), 4);
   cassert(part2("{\"d\": \"red\", \"e\": [1,2,3,4], \"f\": 5}"), 0);
   cassert(part2("[1, \"red\", 3]"), 4);
   console.log("All part2 tests pass");

} else {
  fs.readFile('/storage/emulated/0/wrk/input2015-12.txt', 'utf8' , (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data);
    console.log(`Part 2 result ${res_part2}`);
  })
}
