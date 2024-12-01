let parse_input = (raw_input: string): [number[], number[]] => {
    //const lines = raw_input.split('\n');
    const left: number[] = [];
    const right: number[] = [];
    for (const line of raw_input.split('\n')) {
        const [leftVal, rightVal] = line.split(/\W+/).map((v) => parseInt(v));
        left.push(leftVal);
        right.push(rightVal);
    }
    return [left, right];
};

let part1 = (raw_input: string): number => {
    const [left, right] = parse_input(raw_input);
    left.sort();
    right.sort();
    let diff = 0;
    for (const index in left) {
        diff += Math.abs(left[index] - right[index]);
    }
    return diff;
};

export {
    parse_input,
    part1
}
