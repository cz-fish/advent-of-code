const fs = require("fs");
const assert = require("assert");

function make_matrix(lines, add_self=false) {
    const parse_line = (line) => {
        line = line.replace('.', '');
        const parts = line.split(' ');
        assert(parts.length === 11, `line ${line}, parts ${parts.length}`);
        const p1 = parts[0];
        const p2 = parts[10];
        const gain_lose = parts[2] === 'lose' ? -1 : 1;
        const value = parseInt(parts[3]) * gain_lose;
        return {
            p1,
            p2,
            value
        };
    };

    let records = [];
    for (let line of lines) {
        if (!line) { continue; }
        const rec = parse_line(line);
        records.push(rec);
    }
    const people = [... new Set(records.map(r => r.p1))];
    //console.log(people);

    const num_people = people.length + (add_self ? 1 : 0);

    let matrix = Array(num_people);
    for (let i = 0; i < num_people; ++i) {
        matrix[i] = Array(num_people);
        for (let j = 0; j < num_people; ++j) {
            matrix[i][j] = 0;
        }
    }

    for (let rec of records) {
        const idx1 = people.indexOf(rec.p1);
        const idx2 = people.indexOf(rec.p2);
        matrix[idx1][idx2] += rec.value;
        matrix[idx2][idx1] += rec.value;
    }

    //console.log(matrix);
    return matrix;
}

function evaluate_permutation(seating, n_people, matrix) {
    // map adjacent pair to their mutual happiness, wrapping around for the last one
    return seating.map(
        (v, i) => matrix[v][seating[(i+1) % n_people]]
    ).reduce(
        // sum all up
        (a, v) => a + v
    );
}

function best_permutation(seating, seated, placed, n_people, matrix) {
    let best = undefined;
    for (let person = 1; person < n_people; ++person) {
        if (seated[person]) {
            continue;
        }
        seating[placed] = person;
        if (placed === n_people -1) {
            // Last person was seated
            return evaluate_permutation(seating, n_people, matrix);
        } else {
            seated[person] = true;
            const value = best_permutation(seating, seated, placed + 1, n_people, matrix);
            seated[person] = false;
            best = best === undefined ? value : Math.max(best, value);
        }
    }
    assert(best !== undefined);
    return best;
}

function best_seating_cost(matrix) {
    const n_people = matrix.length;
    assert(n_people > 0);

    let seating = Array(n_people);
    // The table is round, we can choose any pivot.
    // We will place 1st person in 1st position.
    seating[0] = 0;
    let seated = Array(n_people).fill(null)
                                .map((_, i) => {
                                    return i===0 ? true : false;
                                });

    // We will try all permutations of the other persons.
    // Because the table is symmetrical, we would get the same result
    // going clockwise and anti-clockwise, which means that we could
    // reduce the number of tested states by 1/2.
    // But as the input is small enough, it seems that we don't need
    // to bother to optimize.

    return best_permutation(seating, seated, 1, n_people, matrix);
}

function part1(data) {
    const lines = data.split('\n');
    const matrix = make_matrix(lines);
    return best_seating_cost(matrix);
}

function part2(data) {
    const lines = data.split('\n');
    const matrix = make_matrix(lines, true);
    return best_seating_cost(matrix);
}

exports.run = run;
exports.part1 = part1;
exports.part2 = part2;

function run() {
    const data = fs.readFileSync('./input13.txt', 'utf8');

    const res_part1 = part1(data);
    console.log(`Part 1 result ${res_part1}`);
    const res_part2 = part2(data);
    console.log(`Part 2 result ${res_part2}`);
}

if (require.main === module) {
    run();
}
