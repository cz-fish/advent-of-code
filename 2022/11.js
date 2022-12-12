const fs = require("fs");
const assert = require("assert");

class Monkey {
    constructor(items, operation, test, trueMonkey, falseMonkey) {
        this.items = items;
        this.operation = operation;
        this.test = test;
        this.trueMonkey = trueMonkey;
        this.falseMonkey = falseMonkey;
        this.inspCount = 0;
    }
}

function parseOp(opstr) {
    // 'opstr' is "new = old <op> <val>"
    // where <op> can be + or *
    // and <val> is either an integer, or 'old'
    var parts = opstr.split(' ');

    assert(parts.length === 5, `got wrong format ${opstr}`);
    assert(parts[0] === 'new' && parts[1] === '=' && parts[2] === 'old', `got wrong format: ${opstr}`);
    const sign = parts[3];
    assert(sign === '+' || sign === '*', `got operator other than + or *: ${opstr}`);

    const withSelf = (parts[4] === 'old');
    assert(!withSelf || sign === '*', `got "old + old": ${opstr}`);

    if (sign === '+') {
        const val = parseInt(parts[4]);
        return ((v) => {return (x) => x + v;})(val);
    } else {
        if (withSelf) {
            return (x) => x * x;
        } else {
            const val = parseInt(parts[4]);
            return ((v) => {return (x) => x * v;})(val);
        }
    }
}

function parseMonkey(monkeyData) {
    /* monkeyData looks like this:
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
    */

    var items = [];
    var opFunction = null;
    var test = 0;
    var trueMonkey = -1;
    var falseMonkey = -1;
    for (var ln of monkeyData.split('\n')) {
        if (ln.match(/Starting items:/)) {
            items = ln.substr(18).split(', ').map(x => parseInt(x));
        }
        else if (ln.match(/Operation:/)) {
            opFunction = parseOp(ln.substr(13).trim());
        }
        else if (ln.match(/Test: divisible by/)) {
            test = parseInt(ln.substr(20));
        }
        else if (ln.match(/If true/)) {
            trueMonkey = parseInt(ln.substr(28));
        }
        else if (ln.match(/If false/)) {
            falseMonkey = parseInt(ln.substr(29));
        }
    }

    //console.log(`monkey: ${items}, ${opFunction}, ${test}, ${trueMonkey}, ${falseMonkey}`);
    return new Monkey(items, opFunction, test, trueMonkey, falseMonkey);
}

function parseMonkeys(data) {
    return data.split('\n\n').map(m => parseMonkey(m));
}

function getModulus(monkeys) {
    return monkeys.map(m => m.test).reduce((a, b) => a * b);
}

function monkeyTurn(monkey, monkeys, div, mod) {
    for (var item of monkey.items) {
        var value = Math.floor(monkey.operation(item) / div) % mod;
        if (value % monkey.test == 0) {
            monkeys[monkey.trueMonkey].items.push(value);
        } else {
            monkeys[monkey.falseMonkey].items.push(value);
        }
        monkey.inspCount++;
    }
    monkey.items = [];
}

function getMonkeyBusinessLevel(monkeys) {
    var counts = monkeys.map(m => m.inspCount);
    counts = counts.sort((a, b) => (b - a));
    return counts[0] * counts[1];
}

function part1(data) {
    const monkeys = parseMonkeys(data);
    const mod = getModulus(monkeys);
    const div = 3;
    //console.log(`using divider ${div}, modulus ${mod}`);

    const rounds = 20;
    for (var round = 0; round < rounds; ++round) {
        for (var monkey of monkeys) {
            monkeyTurn(monkey, monkeys, div, mod);
        }
    }
    return getMonkeyBusinessLevel(monkeys);
}

function part2(data, silent = true) {
    var monkeys = parseMonkeys(data);
    var mod = getModulus(monkeys);
    var div = 1;
    //console.log(`using divider ${div}, modulus ${mod}`);

    const rounds = 10000;
    const checkpoints = [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000];
    for (var round = 0; round < rounds; ++round) {
        if (!silent && checkpoints.indexOf(round) >= 0) {
            console.log(`  round ${round} ` + JSON.stringify([...monkeys.map(m => m.inspCount)]));
        }
        for (var monkey of monkeys) {
            monkeyTurn(monkey, monkeys, div, mod);
        }
    }
    return getMonkeyBusinessLevel(monkeys);
}

// -- main

function run() {
    const data = fs.readFileSync('./input11.txt', 'utf8');

    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data, false);
    console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

if (require.main === module) {
    run();
}
