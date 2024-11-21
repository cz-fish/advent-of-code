#!/usr/bin/python3.8

from pyaoc import Env
import re

e = Env(21)
e.T("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""", 5, 'mxmxvkd,sqjhc,fvjkl')


def parse_foods(lines):
    foods = []
    for food in lines:
        m = re.match(r'^(.*) \(contains (.*)\)$', food)
        assert m is not None
        ingredients = m.group(1).split(' ')
        allergens = m.group(2).split(', ')
        foods += [(ingredients, allergens)]
    return foods


def match_allergens(foods):
    ale_map = {}
    for ingredients, allergens in foods:
        for al in allergens:
            if al not in ale_map:
                ale_map[al] = set(ingredients)
            else:
                ale_map[al] = ale_map[al] & set(ingredients)

    # sudoku the map
    ale_map_x = {}
    while len(ale_map_x) < len(ale_map):
        keys = list(ale_map.keys())
        for al in keys:
            if al in ale_map_x:
                continue
            ing = ale_map[al]
            if len(ing) == 1:
                ale_map_x[al] = list(ing)[0]
            else:
                ing = ing - set(ale_map_x.values())
                ale_map[al] = ing

    return ale_map_x


def part1(input):
    foods = parse_foods(input.get_valid_lines())
    ale_map = match_allergens(foods)
    bad_stuff = set(ale_map.values())
    count = 0
    for ingr, _ in foods:
        count += len([i for i in ingr if i not in bad_stuff])
    return count


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    foods = parse_foods(input.get_valid_lines())
    ale_map = match_allergens(foods)
    bad_stuff = [(i, a) for (a, i) in ale_map.items()]
    bad_stuff.sort(key=lambda x: x[1])
    return ','.join([x[0] for x in bad_stuff])


e.run_tests(2, part2)
e.run_main(2, part2)
