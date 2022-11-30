const fs = require('fs');
const assert = require('assert');

const rightSue = {
    children: 3,
    cats: 7,
    samoyeds: 2,
    pomeranians: 3,
    akitas: 0,
    vizslas: 0,
    goldfish: 5,
    trees: 3,
    cars: 2,
    perfumes: 1,
};

const num_re = /Sue (?<num>\d+)/;
const prop_re = /(?<prop>\w+): (?<count>\d+)/g;

function make_aunt(line) {
    const sue_num = parseInt(line.match(num_re).groups['num']);
    //console.log(`line "${line}", num: ${sue_num}`);
    sue = {num : sue_num};
    for (var m of [...line.matchAll(prop_re)]) {
        sue[m.groups['prop']] = parseInt(m.groups['count']);
    }
    return sue;
}

function same_aunt_pt1(probe, tgt) {
    for (var prop in probe) {
        if (prop === 'num') {
            continue;
        }
        if (tgt[prop] !== probe[prop]) {
            return false;
        }
    }
    return true;
}

function same_aunt_pt2(probe, tgt) {
    for (var prop in probe) {
        if (prop === 'num') {
            continue;
        }
        if (prop === 'cats' || prop === 'trees') {
            if (tgt[prop] >= probe[prop]) {
                return false;
            }
        } else if (prop === 'pomeranians' || prop === 'goldfish') {
            if (tgt[prop] <= probe[prop]) {
                return false;
            }
        }
        else if (tgt[prop] !== probe[prop]) {
            return false;
        }
    }
    return true;
}

function part1(data) {
    const aunts = data.split('\n')
                      .filter(ln => ln)
                      .map(ln => make_aunt(ln));
    for (var aunt of aunts) {
        if (same_aunt_pt1(aunt, rightSue)) {
            return aunt.num;
        }
    }
    assert(false, "Right Sue was not found");
}

function part2(data) {
    const aunts = data.split('\n')
                      .filter(ln => ln)
                      .map(ln => make_aunt(ln));
    for (var aunt of aunts) {
        if (same_aunt_pt2(aunt, rightSue)) {
            return aunt.num;
        }
    }
    assert(false, "Right Sue was not found");
}

function run() {
    const data = fs.readFileSync('./input16.txt', 'utf8');

    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data);
    console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;
exports.make_aunt = make_aunt;
exports.same_aunt_pt1 = same_aunt_pt1;
exports.same_aunt_pt2 = same_aunt_pt2;

if (require.main === module) {
    run();
}
