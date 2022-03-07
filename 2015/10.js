function expand_n_times(input, iter) {
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


function run() {
	// actual input
	const input = "1113222113";

	const part1_res = expand_n_times(input, 40);
	console.log(`Part 1: ${part1_res.length}`);
	const part2_res = expand_n_times(part1_res, 10);
	console.log(`Part 2: ${part2_res.length}`);
}

exports.run = run
exports.expand_n_times = expand_n_times;

if (require.main === module) {
	run();
}
