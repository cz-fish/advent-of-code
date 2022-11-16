const fs = require("fs");


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

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

function run() {
  const data = fs.readFileSync('./input12.txt', 'utf8');
  const res_part1 = part1(data);
  console.log(`Part 1 result ${res_part1}`);
  const res_part2 = part2(data);
  console.log(`Part 2 result ${res_part2}`);
}

if (require.main === module) {
  run();
}
