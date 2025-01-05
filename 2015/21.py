#!/usr/bin/python3.12

from pyaoc import Env
from dataclasses import dataclass

e = Env(21)


weapons = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]

armors = [
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

rings = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


@dataclass
class Char:
    hp: int
    dmg: int
    armor: int


def is_win(player: Char, boss: Char):
    pl_dmg = max(1, player.dmg - boss.armor)
    boss_dmg = max(1, boss.dmg - player.armor)
    pl_rounds = int(boss.hp / pl_dmg + 0.99)
    boss_rounds = int(player.hp / boss_dmg + 0.99)
    return pl_rounds <= boss_rounds


def part1(input):
    vals = input.get_all_ints()
    assert len(vals) == 3
    boss = Char(hp=int(vals[0]), dmg=int(vals[1]), armor=int(vals[2]))

    """
    for dmg in range(4, 14):
        for armor in range(0, 11):
            player = Char(hp=100, dmg=dmg, armor=armor)
            if is_win(player, boss):
                print(f"Win: dmg {dmg}, armor {armor}")
                break
    """

    min_cost = None
    for weapon_idx in range(len(weapons)):
        for armor_idx in range(-1, len(armors)):
            for ring1_idx in range(-1, len(rings)):
                for ring2_idx in range(-1, len(rings)):
                    if ring2_idx >= 0 and ring2_idx == ring1_idx:
                        continue
                    cost = weapons[weapon_idx][0]
                    dmg = weapons[weapon_idx][1]
                    armor = 0
                    if armor_idx >= 0:
                        cost += armors[armor_idx][0]
                        armor += armors[armor_idx][2]
                    if ring1_idx >= 0:
                        cost += rings[ring1_idx][0]
                        dmg += rings[ring1_idx][1]
                        armor += rings[ring1_idx][2]
                    if ring2_idx >= 0:
                        cost += rings[ring2_idx][0]
                        dmg += rings[ring2_idx][1]
                        armor += rings[ring2_idx][2]
                    if min_cost is not None and cost >= min_cost:
                        continue
                    player = Char(hp=100, dmg=dmg, armor=armor)
                    if is_win(player, boss):
                        if min_cost is None or cost < min_cost:
                            #print(f"cost {cost}: dmg {dmg} armor {armor}, {weapon_idx}, {armor_idx}, {ring1_idx}, {ring2_idx}")
                            min_cost = cost
    return min_cost


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    vals = input.get_all_ints()
    assert len(vals) == 3
    boss = Char(hp=int(vals[0]), dmg=int(vals[1]), armor=int(vals[2]))

    max_cost = None
    for weapon_idx in range(len(weapons)):
        for armor_idx in range(-1, len(armors)):
            for ring1_idx in range(-1, len(rings)):
                for ring2_idx in range(-1, len(rings)):
                    if ring2_idx >= 0 and ring2_idx == ring1_idx:
                        continue
                    cost = weapons[weapon_idx][0]
                    dmg = weapons[weapon_idx][1]
                    armor = 0
                    if armor_idx >= 0:
                        cost += armors[armor_idx][0]
                        armor += armors[armor_idx][2]
                    if ring1_idx >= 0:
                        cost += rings[ring1_idx][0]
                        dmg += rings[ring1_idx][1]
                        armor += rings[ring1_idx][2]
                    if ring2_idx >= 0:
                        cost += rings[ring2_idx][0]
                        dmg += rings[ring2_idx][1]
                        armor += rings[ring2_idx][2]
                    if max_cost is not None and cost < max_cost:
                        continue
                    player = Char(hp=100, dmg=dmg, armor=armor)
                    if not is_win(player, boss):
                        if max_cost is None or cost > max_cost:
                            #print(f"cost {cost}: dmg {dmg} armor {armor}, {weapon_idx}, {armor_idx}, {ring1_idx}, {ring2_idx}")
                            max_cost = cost
    return max_cost


e.run_tests(2, part2)
e.run_main(2, part2)
