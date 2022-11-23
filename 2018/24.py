#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict

e = Env(24)
e.T("""Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""",
    5216,
    51,
    param='test')

IS = 'IS'
INF = 'INF'

class Group:
    def __init__(self, army, id, units, hp, immune, weak, atk, atk_type, initiative):
        self.army = army
        self.id = id
        self.units = units
        self.hp = hp
        self.immune = immune
        self.weak = weak
        self.atk = atk
        self.atk_type = atk_type
        self.initiative = initiative
    
    def copy_with_boost(self, boost):
        return Group(self.army, self.id, self.units, self.hp, self.immune, self.weak, self.atk + boost, self.atk_type, self.initiative)

    def power(self):
        return self.units * self.atk

    @classmethod
    def make(cls, line, army, id):
        modifiers = ''
        bracket = line.find('(')
        if bracket != -1:
            bracket_end = line.find(')')
            assert bracket_end != '-1', f"Line '{line}' has opening bracket but no closing"
            modifiers = line[bracket+1 : bracket_end]
            line = line[:bracket] + line[bracket_end + 2:]
        parts = line.split(' ')
        assert len(parts) == 18, f"Line '{line}' doesn't have 18 fields"
        units = int(parts[0])
        hp = int(parts[4])
        atk = int(parts[12])
        atk_type = parts[13]
        initiative = int(parts[17])
        mods = modifiers.split('; ')
        immune = []
        weak = []
        for mod in mods:
            if not mod:
                continue
            mod = mod.replace(',', '')
            parts = mod.split(' ')
            assert len(parts) >= 3 and parts[0] in ['immune', 'weak'], f"broken line: {line}, {bracket}, {modifiers}, {parts}"
            if parts[0] == 'weak':
                weak = parts[2:]
            else:
                immune = parts[2:]
        return Group(army, id, units, hp, immune, weak, atk, atk_type, initiative)

    def __repr__(self):
        return f"[{self.army} {self.id}, power={self.power()}, units={self.units}, hp={self.hp}, atk={self.atk}, init={self.initiative}, atk_type={self.atk_type}, immune={self.immune}, weak={self.weak}]"


def make_armies(input):
    army = None
    army_groups = defaultdict(list)
    for ln in input.get_valid_lines():
        if ln == 'Immune System:':
            army = IS
            counter = 1
        elif ln == 'Infection:':
            army = INF
            counter = 1
        elif ln == '':
            continue
        else:
            assert army is not None, "group without an army"
            group = Group.make(ln, army, counter)
            counter += 1
            army_groups[army].append(group)
    # print(army_groups)
    return army_groups


def calculate_damage(attackers, defenders):
    if attackers.atk_type in defenders.immune:
        return 0
    base_dmg = attackers.units * attackers.atk
    if attackers.atk_type in defenders.weak:
        return 2 * base_dmg
    return base_dmg


def find_best_target(group, enemies, used):
    best_dmg = 0
    best_power = 0
    best_initiative = 0
    best_index = None
    for i, enemy in enumerate(enemies):
        if i in used:
            continue
        dmg = calculate_damage(group, enemy)
        if dmg == 0:
            continue
        if dmg > best_dmg or\
           (dmg == best_dmg and enemy.power() > best_power) or \
           (dmg == best_dmg and enemy.power() == best_power and enemy.initiative > best_initiative):
            best_dmg = dmg
            best_index = i
            best_power = enemy.power()
            best_initiative = enemy.initiative
    if best_index is not None:
        used.add(best_index)
    return best_index


def choose_targets(atk_army, def_army):
    order = [(g.power(), g.initiative, i) for i, g in enumerate(atk_army)]
    order.sort(reverse=True)
    targeted = set()
    targets = [None for _ in order]
    for (_, _, i) in order:
        targets[i] = find_best_target(atk_army[i], def_army, targeted)
    return targets


def battle_round(armies):
    assert IS in armies and INF in armies
    targets = {
        IS: choose_targets(armies[IS], armies[INF]),
        INF: choose_targets(armies[INF], armies[IS])
    }
    all_groups = []
    for army in armies.keys():
        for i, group in enumerate(armies[army]):
            all_groups.append((group.initiative, army, i, group))
    # attack in order of initiative
    tie = True
    all_groups.sort(reverse=True)
    for (_, army, index, group) in all_groups:
        if group.units <= 0:
            # group already killed
            continue
        target_idx = targets[army][index]
        if target_idx is None:
            # no target for this group
            continue
        enemy_army = INF if army == IS else IS
        target_group = armies[enemy_army][target_idx]
        dmg = calculate_damage(group, target_group)
        units_killed = min(target_group.units, dmg // target_group.hp)
        target_group.units -= units_killed
        if units_killed > 0:
            tie = False
        #print(f"{army} group {index} deals {dmg} dmg to {enemy_army} group {target_idx} and kills {units_killed} units")

    if tie:
        # nobody killed anybody; this would be a tie
        return {}

    # return remaining armies
    remaining_is = [g for g in armies[IS] if g.units > 0]
    remaining_inf = [g for g in armies[INF] if g.units > 0]
    result = {}
    if remaining_is:
        result[IS] = remaining_is
    if remaining_inf:
        result[INF] = remaining_inf
    return result


def print_armies(armies):
    for groups in armies.values():
        for g in groups:
            print(g)


def part1(input):
    armies = make_armies(input)
    # print_armies(armies)
    round = 0
    while len(armies) == 2:
        armies = battle_round(armies)
        round += 1
        #print(f"After round {round}")
        #print_armies(armies)
    print(f"Finished after {round} rounds")
    # print_armies(armies)
    assert len(armies) == 1, f"Got a tie. {len(armies)} armies at the end of the battle"
    winners = list(armies.values())[0]
    return sum([group.units for group in winners])


e.run_tests(1, part1)
e.run_main(1, part1)

def copy_armies_with_boost(original_armies, boost):
    armies = {
        IS: [],
        INF: []
    }
    for group in original_armies[IS]:
        armies[IS].append(group.copy_with_boost(boost))
    for group in original_armies[INF]:
        armies[INF].append(group.copy_with_boost(0))
    return armies


def run_with_boost(original_armies, boost):
    armies = copy_armies_with_boost(original_armies, boost)
    while len(armies) == 2:
        armies = battle_round(armies)
    if IS not in armies:
        # Either IS lost, or there was a tie, which is as good as a loss
        return 0
    return sum([group.units for group in armies[IS]])


def part2(input):
    is_test = e.get_param() == 'test'
    armies = make_armies(input)
    min_boost = 0
    max_boost = 20000
    assert run_with_boost(armies, min_boost) == 0, "Already won without any boost"
    assert run_with_boost(armies, max_boost) > 0, f"Max boost too low, cannot win with boost={max_boost}"
    while max_boost - min_boost > 1:
        boost = (max_boost + min_boost) // 2
        res = run_with_boost(armies, boost)
        if not is_test:
            print(f"Boost [{min_boost} {boost} {max_boost}], result {res}")
        if res > 0:
            max_boost = boost
        else:
            min_boost = boost
    return run_with_boost(armies, max_boost)


e.run_tests(2, part2)
e.run_main(2, part2)
