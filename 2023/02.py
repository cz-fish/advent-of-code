#!/usr/bin/python3.8

from pyaoc import Env

e = Env(2)
e.T("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 8, 2286)

def parse_games(lines):
    games = []
    # Assuming that games are ordered and starting from game 1, as in the sample input
    for ln in lines:
        game = []
        _, conf = ln.split(': ', 1)
        shows = conf.split('; ')
        for show in shows:
            colors = show.split(', ')
            red = 0
            green = 0
            blue = 0
            for color in colors:
                v, c = color.split(' ')
                val = int(v)
                if c == 'red':
                    red = val
                elif c == 'green':
                    green = val
                elif c == 'blue':
                    blue = val
                else:
                    assert False, f"Unknown color {c} on line '{ln}' in show '{show}'"
            game.append((red, green, blue))
        games.append(game)
    return games


def part1(input):
    limits = (12, 13, 14)
    lines = input.get_valid_lines()
    games = parse_games(lines)
    return sum([
        i + 1
        for i, game in enumerate(games)
        if all([r <= limits[0] and g <= limits[1] and b <= limits[2] for r, g, b in game])
    ])


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    lines = input.get_valid_lines()
    games = parse_games(lines)
    powers = 0
    for game in games:
        mr = max([s[0] for s in game])
        mg = max([s[1] for s in game])
        mb = max([s[2] for s in game])
        powers += mr * mg * mb
    return powers


e.run_tests(2, part2)
e.run_main(2, part2)
