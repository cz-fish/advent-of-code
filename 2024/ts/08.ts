type Pos = [number, number];

class Grid {
    width: number = 0;
    height: number = 0;
    antennas: Map<string, Pos[]> = new Map();
}

const parse_input = (raw_input: string): Grid => {
    const grid = new Grid();
    let row = 0;
    for (let ln of raw_input.split('\n')) {
        ln = ln.trim();
        if (!ln) {
            break;
        }
        if (grid.width === 0) {
            grid.width = ln.length;
        } else {
            console.assert(grid.width === ln.length, `rows of different lengths: ${grid.width} and ${ln.length}`);
        }
        grid.height++;
        for (let i = 0; i < grid.width; ++i) {
            const c = ln[i];
            if (c !== '.') {
                if (!grid.antennas.has(c)) {
                    grid.antennas.set(c, []);
                }
                grid.antennas.get(c)?.push([row, i]);
            }
        }
        row++;
    }
    return grid;
}

const get_antenna_pairs = (grid: Grid): [Pos, Pos][] => {
    const pairs: [Pos, Pos][] = [];
    for (const points of grid.antennas.values()) {
        for (let i = 0; i < points.length; ++i) {
            for (let j = i + 1; j < points.length; ++j) {
                pairs.push([points[i], points[j]]);
            }
        }
    }
    return pairs;
}

const find_antinodes = (grid: Grid, resonance: boolean): Set<number> => {
    const pairs = get_antenna_pairs(grid);
    // Note - using a set of numbers, where each number is row*width+col.
    // Cannot use tuples/pairs of [row, col], because Set keys are compared
    // by object reference equality, not by values.
    const antinodes = new Set<number>();
    for (const [first, second] of pairs) {
        const d_row = second[0] - first[0];
        const d_col = second[1] - first[1];
        let nr = first[0] - d_row;
        let nc = first[1] - d_col;
        while (nr >= 0 && nc >= 0 && nr < grid.height && nc < grid.width) {
            antinodes.add(nr * grid.width + nc);
            if (!resonance) {
                break;
            }
            nr -= d_row;
            nc -= d_col;
        }
        nr = second[0] + d_row;
        nc = second[1] + d_col;
        while (nr >= 0 && nc >= 0 && nr < grid.height && nc < grid.width) {
            antinodes.add(nr * grid.width + nc);
            if (!resonance) {
                break;
            }
            nr += d_row;
            nc += d_col;
        }
        if (resonance) {
            antinodes.add(first[0] * grid.width + first[1]);
            antinodes.add(second[0] * grid.width + second[1]);
        }
    }
    return antinodes;
}

const part1 = (raw_input: string): number => {
    const grid = parse_input(raw_input);
    const antinodes = find_antinodes(grid, false);
    return antinodes.size;
}

const part2 = (raw_input: string): number => {
    const grid = parse_input(raw_input);
    const antinodes = find_antinodes(grid, true);
    return antinodes.size;
}

export {
    Grid,
    find_antinodes,
    get_antenna_pairs,
    parse_input,
    part1,
    part2,
}
