const parse_input = (raw_input: string): string[] => {
    const grid: string[] = [];
    let row = 0;
    for (let ln of raw_input.split('\n')) {
        ln = ln.trim();
        if (!ln) {
            break;
        }
        grid.push(ln);
        row++;
    }
    return grid;
}

const count_xmas_in_8_directions = (grid: string[], row: number, col: number): number => {
    let count = 0;
    for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1], [-1, -1], [-1, 1], [1, -1], [1, 1]]) {
        const er = row + 3 * dr;
        const ec = col + 3 * dc;
        if (er < 0 || ec < 0 || er >= grid.length || ec >= grid[0].length) {
            continue;
        }
        const s = grid[row][col] + grid[row+dr][col+dc] + grid[row+2*dr][col+2*dc] + grid[er][ec];
        if (s === "XMAS") {
            count++;
        }
    }
    return count;
}

const count_xmas = (grid: string[]): number => {
    let count = 0;
    for (let row = 0; row < grid.length; ++row) {
        for (let col = 0; col < grid[row].length; ++col) {
            if (grid[row][col] === 'X') {
                count += count_xmas_in_8_directions(grid, row, col);
            }
        }
    }
    return count;
}

const count_x_mas = (grid: string[]): [number, number][] => {
    let pos: [number, number][] = [];
    for (let row = 1; row < grid.length - 1; ++row) {
        for (let col = 1; col < grid[row].length - 1; ++col) {
            if (grid[row][col] === 'A') {
                const diag1 = grid[row-1][col-1] + 'A' + grid[row+1][col+1];
                if (diag1 !== "MAS" && diag1 !== "SAM") {
                    continue;
                }
                const diag2 = grid[row-1][col+1] + 'A' + grid[row+1][col-1];
                if (diag2 === "MAS" || diag2 === "SAM") {
                    pos.push([row, col]);
                }
            }
        }
    }
    return pos;
}

const part1 = (raw_input: string): number => {
    const grid = parse_input(raw_input);
    return count_xmas(grid);
}

const part2 = (raw_input: string): number => {
    const grid = parse_input(raw_input);
    return count_x_mas(grid).length;
}

export {
    count_x_mas,
    parse_input,
    part1,
    part2,
}
