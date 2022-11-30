const fs = require('fs');

function part1(data) {
}

function part2(data) {
}

function run() {
    const data = fs.readFileSync('./input0.txt', 'utf8');

    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data);
    console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

if (require.main === module) {
    run();
}
