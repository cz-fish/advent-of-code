const fs = require("fs");
const assert = require("assert");

function parseInput(data) {
    return data.split('\n').map(ln => ln.split(' '));
}

function decodeInstruction(instr) {
    var valueAdd = 0;
    var timeSkip = 1
    if (instr[0] === 'addx') {
        valueAdd = parseInt(instr[1]);
        timeSkip = 2;
    }
    return {timeSkip, valueAdd};
}

function part1(data) {
    const instructions = parseInput(data);

    var x = 1;
    var cycle = 0;
    var next_mark = 20;
    var signal = 0;
    for (var instr of instructions) {
        const {timeSkip, valueAdd} = decodeInstruction(instr);
        const new_cycle = cycle + timeSkip;
        if (new_cycle >= next_mark) {
            signal += next_mark * x;
            // console.log(`${next_mark}: ${x} -> ${next_mark * x} (${signal})`);
            next_mark += 40;
        }
        x += valueAdd;
        cycle = new_cycle;
    }
    return signal;
}

function part2(data) {
    const instructions = parseInput(data);

    const HEIGHT = 6;
    const WIDTH = 40;

    var screen = [];
    for (var y = 0; y < HEIGHT; ++y) {
        screen.push([]);
        for (var x = 0; x < WIDTH; ++x) {
            screen[y].push('.');
        }
    }

    var cycle = 0;
    var x = 1;

    for (var instr of instructions) {
        const {timeSkip, valueAdd} = decodeInstruction(instr);
        for (var iCycle = 0; iCycle < timeSkip; iCycle++) {
            const col = cycle % WIDTH;
            const row = Math.floor(cycle / WIDTH);
            if (row >= HEIGHT) {
                // out of the screen
                continue;
            }
            if (col >= x - 1 && col <= x + 1) {
                // sprite is at the ray (+- one pixel)
                screen[row][col] = '#';
            }
            cycle++;
        }
        x += valueAdd;
    }

    return screen.map(row => row.join('')).join('\n');
}

// -- main

function run() {
    const data = fs.readFileSync('./input10.txt', 'utf8');

    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data);
    console.log(`Part 2 result\n${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

if (require.main === module) {
    run();
}
