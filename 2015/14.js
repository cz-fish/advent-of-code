const assert = require('assert');
const fs = require('fs');

function parse_input(input) {
    const pat = /^(?<name>\w+) can fly (?<speed>\d+) km\/s for (?<time>\d+) seconds, but then must rest for (?<rest>\d+) seconds./;
    var deers = Array();
    for (const line of input.split('\n')) {
        if (!line) {
            continue;
        }
        const m = line.match(pat);
        assert(m !== null, `Input line doesn't match: ${line}`);
        deers.push({
            name: m.groups.name,
            speed: parseInt(m.groups.speed),
            time: parseInt(m.groups.time),
            rest: parseInt(m.groups.rest),
        });
    }
    return deers;
}

function fly(deer, time) {
    const one_period = deer.time + deer.rest;
    const periods = Math.floor(time / one_period);
    const remain = time - periods * one_period;
    const rem_dist = Math.min(remain, deer.time) * deer.speed;
    return periods * deer.time * deer.speed + rem_dist;
}

function part1(input, time) {
    const deers = parse_input(input);
    // console.log(deers);
    const dists = deers.map(d => fly(d, time));
    // console.log(dists);
    return dists.reduce((a, b) => Math.max(a, b));
}

function fly_bunch(deers, time) {
    const race = deers.map((deer, index) => { return {
        points: 0,
        dist: 0,
        left_to_fly: deer.time,
        left_to_rest: 0,
    }; });
    const num_deers = race.length;
    // After each second
    for (var t = 1; t <= time; ++t) {
        // Update all deers by 1 second
        for (var i = 0; i < num_deers; ++i) {
            const state = race[i];
            const deer = deers[i];
            if (state.left_to_fly > 0) {
                state.dist += deer.speed;
                state.left_to_fly--;
                if (state.left_to_fly === 0) {
                    state.left_to_rest = deer.rest;
                }
            } else {
                assert(state.left_to_rest > 0);
                state.left_to_rest--;
                if (state.left_to_rest === 0) {
                    state.left_to_fly = deer.time;
                }
            }
        }

        // Find leader
        const leader = race.reduce((a, b) => a.dist > b.dist ? a : b);
        // Give leader(s) a point
        race.forEach(state => {
            if (state.dist === leader.dist) {
                state.points++;
            }
        });
    }

    // console.log(race);

    // Find winner's points
    return race.reduce((a, b) => a.points > b.points ? a : b).points;
}

function part2(input, time) {
    const deers = parse_input(input);
    return fly_bunch(deers, time);
}

function run() {
    const data = fs.readFileSync('./input14.txt', 'utf8');

    const end_time = 2503;
    const res_part1 = part1(data, end_time);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data, end_time);
    console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

if (require.main === module) {
    run();
}
