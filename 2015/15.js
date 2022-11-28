const fs = require('fs');
const assert = require('assert');

function make_ingredients(data) {
    const number_re = /-?\d+/g;
    return data.split('\n').filter(x => x).map(ln => {
        const numbers = [...ln.matchAll(number_re)].map(x => parseInt(x[0]));
        assert(numbers.length === 5, `Wrong number of parameters (${numbers.length}) in "${ln}"`);
        return {
            profile: numbers.slice(0, 4),
            calories: numbers[4],
        };
    });
}

function profile_cost(ingredients, taken, calorie_check) {
    if (calorie_check !== undefined) {
        const calories = taken.map((t, i) => ingredients[i].calories * t).reduce((a, b) => a + b);
        if (calories !== calorie_check) {
            return 0;
        }
    }
    const nutrients = ingredients[0].profile.length;
    var result = 1;
    for (var n = 0; n < nutrients; ++n) {
        var sum = taken.map((t, i) => ingredients[i].profile[n] * t).reduce((a, b) => a + b);
        sum = Math.max(0, sum);
        result *= sum;
    }
    return result;
}

function take_ingredient(ingredients, ing_taken, spoons_remaining, calorie_check) {
    if (ing_taken.length === ingredients.length - 1) {
        // last ingredient. Take `spoons_remaining`
        ing_taken.push(spoons_remaining);
        const cost = profile_cost(ingredients, ing_taken, calorie_check);
        ing_taken.pop();
        return cost;
    }
    var best_cost = 0;
    for (var take = 0; take <= spoons_remaining; take++) {
        ing_taken.push(take);
        best_cost = Math.max(best_cost, take_ingredient(ingredients, ing_taken, spoons_remaining - take, calorie_check));
        ing_taken.pop();
    }
    return best_cost;
}

function part1(data) {
    const teaspoons = 100;
    const ingredients = make_ingredients(data);
    //console.log(ingredients);
    return take_ingredient(ingredients, [], teaspoons);
}

function part2(data) {
    const teaspoons = 100;
    const ingredients = make_ingredients(data);
    //console.log(ingredients);
    return take_ingredient(ingredients, [], teaspoons, 500);
}

function run() {
    const data = fs.readFileSync('./input15.txt', 'utf8');

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
