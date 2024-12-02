let parse_input = (raw_input) => {
    const left = [];
    const right = [];
    for (const line of raw_input.split('\n')) {
        if (!line.trim()) {
            continue;
        }
        const [leftVal, rightVal] = line.split(/\W+/).map(v => parseInt(v));
        left.push(leftVal);
        right.push(rightVal);
    }
    return [left, right];
};
let part1 = (raw_input) => {
    const [left, right] = parse_input(raw_input);
    left.sort();
    right.sort();
    let diff = 0;
    for (const index in left) {
        diff += Math.abs(left[index] - right[index]);
    }
    return diff;
};
let part2 = (raw_input) => {
    var _a;
    const [left, right] = parse_input(raw_input);
    const counters = new Map();
    for (const v of right) {
        counters.set(v, ((_a = counters.get(v)) !== null && _a !== void 0 ? _a : 0) + 1);
    }
    return left.map(v => { var _a; return v * ((_a = counters.get(v)) !== null && _a !== void 0 ? _a : 0); }).reduce((a, v) => a + v);
};
export { parse_input, part1, part2, };
