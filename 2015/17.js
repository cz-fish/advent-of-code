const fs = require('fs');
const assert = require('assert');

function fill_next(numbers, i, remain, used, counters) {
    if (remain === 0) {
        // target reached
        counters.set(used, (counters.get(used) ?? 0) + 1);
        return;
    }
    if (i === numbers.length) {
        // already took all items and target not reached
        return;
    }

    if (numbers[i] <= remain) {
        // take i-th item
        fill_next(numbers, i + 1, remain - numbers[i], used + 1, counters);
    }
    // do not take i-th item
    fill_next(numbers, i + 1, remain, used, counters);
}

function part1(numbers, target) {
    let counters = new Map();
    fill_next(numbers, 0, target, 0, counters);
    return [...counters.values()].reduce((a, b) => a + b);
}

function part2(numbers, target) {
    let counters = new Map();
    fill_next(numbers, 0, target, 0, counters);
    assert(counters.size > 0);
    const least_pots = [...counters.keys()].reduce((a, b) => a < b? a : b);
    return counters.get(least_pots);
}

function run() {
    const data = fs.readFileSync('./input17.txt', 'utf8');
    const numbers = data.split('\n').filter(x => x).map(x => parseInt(x));
    const target = 150;

    const res_part1 = part1(numbers, target);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(numbers, target);
    console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

if (require.main === module) {
    run();
}
