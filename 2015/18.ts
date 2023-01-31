const fs = require('fs');
const assert = require('assert');

const count_lights = (grid: number[][]): number => {
    let total = 0;
    grid.forEach(row => {
        total += row.reduce((c, v) => c + v);
    });
    return total;
}

const one_iteration = (grid: number[][], corners_stuck: boolean): number[][] => {
    const height = grid.length;
    const width = grid[0].length;

    const count_neighbors = (row_idx, col_idx) => {
        let count = 0;
        for (let dx = -1; dx <= 1; ++dx) {
            for (let dy = -1; dy <= 1; ++dy) {
                if (dx === 0 && dy === 0) {
                    continue;
                }
                const nx = col_idx + dx;
                const ny = row_idx + dy;
                if (nx < 0 || ny < 0 || nx >= width || ny >= height) {
                    continue;
                }
                count += grid[ny][nx];
            }
        }
        return count;
    };

    const new_grid: number[][] = [];
    for (let row_idx = 0; row_idx < height; ++row_idx) {
        const row: number[] = [];
        for (let col_idx = 0; col_idx < width; ++col_idx) {
            if (corners_stuck
                && (row_idx === 0 || row_idx === height-1)
                && (col_idx === 0 || col_idx === width-1)) {
                // corners are stuck on
                row.push(1);
            } else {
                const neighbors = count_neighbors(row_idx, col_idx);
                const alive = grid[row_idx][col_idx] === 1;
                if (alive && (neighbors < 2 || neighbors > 3)) {
                    // turn off
                    row.push(0);
                } else if (!alive && neighbors === 3) {
                    // turn on
                    row.push(1);
                } else  {
                    row.push(grid[row_idx][col_idx]);
                }
            }
        }
        new_grid.push(row);
    }

    return new_grid;
}

const print_grid = (grid: number[][]) => {
    let s = "";
    grid.forEach(row => {
        s += row.map(v => '.#'.charAt(v)).join(' ') + "\n";
    });
    console.log(s);
}

const run_game = (text: string, steps: number, corners_stuck: boolean): number => {
    const lines = text.split('\n').filter(ln => ln.length > 0);
    let grid: number[][] = [];
    lines.forEach(line => {
        const row = Array.from(line).map(ch => ch === '#' ? 1 : 0);
        grid.push(row);
    });
    if (corners_stuck) {
        const height = grid.length;
        const width = grid[0].length;
        grid[0][0] = 1;
        grid[0][width-1] = 1;
        grid[height-1][0] = 1;
        grid[height-1][width-1] = 1;
    }

    for (let step = 0; step < steps; ++step) {
        grid = one_iteration(grid, corners_stuck);

        /*
        console.log(`After step ${step + 1}`);
        print_grid(grid);
        */
    }
    print_grid(grid);

    return count_lights(grid);
}

const part1 = (text: string, steps: number): number => {
    return run_game(text, steps, false);
}

const part2 = (text: string, steps: number): number => {
    return run_game(text, steps, true);
}

const run = () => {
    const data = fs.readFileSync('./input18.txt', 'utf8');
    const flashes1 = part1(data, 100);
    console.log(`Part 1: ${flashes1}`);
    const flashes2 = part2(data, 100);
    console.log(`Part 2: ${flashes2}`);
}

if (require.main === module) {
    run();
}

export {
    run,
    part1,
    part2,
};
