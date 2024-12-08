const parse_input = (raw_input) => {
    const rows = [];
    for (let line of raw_input.split('\n')) {
        line = line.trim();
        if (!line) {
            continue;
        }
        rows.push(line.split(' ').map(v => parseInt(v)));
    }
    return rows;
};
const is_correct_seqence = (row) => {
    const diffs = [...row.keys()].slice(0, row.length - 1).map((index) => row[index] - row[index + 1]);
    return diffs.every((v) => v > 0 && v <= 3) || diffs.every((v) => v < 0 && v >= -3);
};
const part1 = (raw_input) => {
    return parse_input(raw_input).filter(is_correct_seqence).length;
};
// @returns true if the row is correct or can be corrected, false otherwise,
//          and the value to be removed to make it correct, if any.
const maybe_remove_one = (row) => {
    if (is_correct_seqence(row)) {
        // already correct
        return [true, undefined];
    }
    for (let index = 0; index < row.length; ++index) {
        const sub_row = row.slice(0, index).concat(row.slice(index + 1));
        if (is_correct_seqence(sub_row)) {
            // correct after removing values at index
            return [true, row[index]];
        }
    }
    // cannot be corrected
    return [false, undefined];
};
const part2 = (raw_input) => {
    return parse_input(raw_input).map((row) => maybe_remove_one(row)[0]).filter((v) => v).length;
};
export { maybe_remove_one, parse_input, part1, part2, };
