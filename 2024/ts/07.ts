type ParsedNumbers = [number, number[]];

const parse_input = (raw_input: string): ParsedNumbers[] => {
    const formulas: ParsedNumbers[] = [];
    for (let line of raw_input.split('\n')) {
        line = line.trim();
        if (!line) {
            continue;
        }
        const [left, right] = line.split(": ")
        formulas.push([parseInt(left), right.split(' ').map(v => parseInt(v))]);
    }
    return formulas;
}

const make_formula = (target: number,
                      vals: number[],
                      pos: number,
                      running_total: number,
                      use_concat: boolean,
                      expr_so_far: string): [boolean, string | undefined] => {
    if (pos === vals.length) {
        if (running_total === target) {
            return [true, expr_so_far];
        } else {
            return [false, undefined];
        }
    }
    if (running_total > target) {
        return [false, undefined];
    }
    let [success, resp] = make_formula(target, vals, pos + 1, running_total + vals[pos], use_concat, expr_so_far + " + " + vals[pos]);
    if (success) { return [true, resp]; }
    [success, resp] = make_formula(target, vals, pos + 1, running_total * vals[pos], use_concat, expr_so_far + " * " + vals[pos]);
    if (success) { return [true, resp]; }
    if (use_concat) {
        [success, resp] = make_formula(target, vals, pos + 1, parseInt("" + running_total + vals[pos]), use_concat, expr_so_far + " || " + vals[pos]);
        if (success) { return [true, resp]; }
    }
    return [false, undefined];
}

const part1 = (raw_input: string): number => {
    const formulas = parse_input(raw_input);
    let sum = 0;
    for (const [target, vals] of formulas) {
        const [success, repr] = make_formula(target, vals, 1, vals[0], false, "" + vals[0]);
        if (success) {
            sum += target;
        }
    }
    return sum;
}

const part2 = (raw_input: string): number => {
    const formulas = parse_input(raw_input);
    let sum = 0;
    for (const [target, vals] of formulas) {
        const [success, repr] = make_formula(target, vals, 1, vals[0], true, "" + vals[0]);
        if (success) {
            sum += target;
        }
    }
    return sum;
}

export {
    make_formula,
    parse_input,
    part1,
    part2,
}
