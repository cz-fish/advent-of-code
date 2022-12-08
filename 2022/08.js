const fs = require('fs');
const assert = require('assert');

class Dir {
    constructor(start_row, start_col, d_row, d_col) {
        this.start_row = start_row;
        this.start_col = start_col;
        this.d_row = d_row;
        this.d_col = d_col;
    }
}

function look_in_direction(rows, height, width, vis, dir)
{
    let prev = -1;
    let row = dir.start_row;
    let col = dir.start_col;
    while (row >= 0 && row < height && col >= 0 && col < width) {
        const v = parseInt(rows[row].charAt(col));
        if (v > prev) {
            vis[row * width + col] = 1;
            prev = v;
            if (v === 9) {
                // 9 is already highest, no need to continue
                return;
            }
        }
        row += dir.d_row;
        col += dir.d_col;
    }
}

function count_visible(rows) {
    const height = rows.length;
    assert(height > 0);
    const width = rows[0].length;
    const vis = new Array(height * width, );

    for (var start_row = 0; start_row < height; ++start_row) {
        // left to right
        look_in_direction(rows, height, width, vis, new Dir(start_row, 0, 0, 1));
        // right to left
        look_in_direction(rows, height, width, vis, new Dir(start_row, width-1, 0, -1));
    }

    for (var start_col = 0; start_col < width; ++start_col) {
        // top to bottom
        look_in_direction(rows, height, width, vis, new Dir(0, start_col, 1, 0));
        // bottom to top
        look_in_direction(rows, height, width, vis, new Dir(height-1, start_col, -1, 0));
    }
    // count ones in vis
    return vis.filter(x => x === 1).length;
}

function part1(data) {
    const rows = data.split('\n').filter(x => x);
    return count_visible(rows);
}

// ---- part 2

function score_in_direction(rows, height, width, scores, dir)
{
    // for each tree height, how far can it see?
    let dist_by_height = new Array(10).fill(0);
    let row = dir.start_row;
    let col = dir.start_col;
    let steps = 0;
    while (row >= 0 && row < height && col >= 0 && col < width) {
        const v = parseInt(rows[row].charAt(col));
        const view = steps - dist_by_height[v];
        scores[row * width + col] *= view;
        for (var i = 0; i <= v; i++) {
            dist_by_height[i] = steps;
        }
        steps++;
        row += dir.d_row;
        col += dir.d_col;
    }
}

function find_best_scenic_score(rows) {
    const height = rows.length;
    assert(height > 0);
    const width = rows[0].length;
    const scores = new Array(height * width).fill(1);

    for (var start_row = 0; start_row < height; ++start_row) {
        // left to right
        score_in_direction(rows, height, width, scores, new Dir(start_row, 0, 0, 1));
        // right to left
        score_in_direction(rows, height, width, scores, new Dir(start_row, width-1, 0, -1));
    }

    for (var start_col = 0; start_col < width; ++start_col) {
        // top to bottom
        score_in_direction(rows, height, width, scores, new Dir(0, start_col, 1, 0));
        // bottom to top
        score_in_direction(rows, height, width, scores, new Dir(height-1, start_col, -1, 0));
    }
    // find highest value in scores
    return scores.reduce((a, b) => (a > b ? a : b));
}

function part2(data) {
    const rows = data.split('\n').filter(x => x);
    return find_best_scenic_score(rows);
}

// -- main

function run() {
    const data = fs.readFileSync('./input08.txt', 'utf8');

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
