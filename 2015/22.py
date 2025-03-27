#!/usr/bin/python3.12

from pyaoc import Env
from dataclasses import dataclass
import heapq


@dataclass
class Setup:
    hp: int
    mana: int


e = Env(22, param=Setup(hp=50, mana=500))

# hp 10
# mana 250
# boss 13
# dmg 8
# -- poison for 173, missile for 53
e.T("""Hit Points: 13
Damage: 8""", 173+53, None, param=(Setup(hp=10, mana=250)))

# hp 10
# mana 250
# boss 14
# dmg 8
# -- rech for 229, shield for 113, drain for 73, poison for 173, missile for 53
# costs: 229, 342, 415, 588, 641
e.T("""Hit Points: 14
Damage: 8""", 229+113+73+173+53, None, param=(Setup(hp=10, mana=250)))


@dataclass
class Spell:
    cost: int
    dmg: int
    heal: int
    armor: int
    lasts: int
    mana_gain: int

    def __repr__(self):
        s = f"lasts {self.lasts}"
        if self.dmg > 0:
            s += f", dmg {self.dmg}"
        if self.heal > 0:
            s += f", heal {self.heal}"
        if self.armor > 0:
            s += f", armor {self.armor}"
        if self.mana_gain > 0:
            s += f", mana_gain {self.mana_gain}"
        return s


spells = [
    Spell(cost=53, dmg=4, heal=0, armor=0, lasts=1, mana_gain=0),
    Spell(cost=73, dmg=2, heal=2, armor=0, lasts=1, mana_gain=0),
    Spell(cost=113, dmg=0, heal=0, armor=7, lasts=6, mana_gain=0),
    Spell(cost=173, dmg=3, heal=0, armor=0, lasts=6, mana_gain=0),
    Spell(cost=229, dmg=0, heal=0, armor=0, lasts=5, mana_gain=101),
]


@dataclass
class State:
    hp: int
    mana: int
    armor: int
    bhp: int
    player_turn: bool
    effects: list

    def __lt__(self, other):
        return self.bhp < other.bhp


def print_state(cost, state):
    print(f"cost {cost}: [hp {state.hp}, mana {state.mana}] [bhp {state.bhp}] {state.player_turn} {len(state.effects)}")


def apply_effects(state: State):
    new_effects = []
    for i, effect in enumerate(state.effects):
        #print(f"  apply {effect}")
        state.bhp -= effect.dmg
        state.hp += effect.heal
        if effect.armor > 0:
            state.armor = effect.armor
        state.mana += effect.mana_gain
        effect.lasts -= 1
        if effect.lasts == 0:
            # Reset armor if expired
            if effect.armor > 0:
                state.armor = 0
        else:
            new_effects.append(effect)
    state.effects = new_effects


def spell_not_active(effects, spell):
    # All costs are different. Check that there
    # is no spell with the same cost as the one we
    # want to cast in current effects
    return not any([e for e in effects if e.cost == spell.cost])


def copy_spell(spell: Spell) -> Spell:
    return Spell(
        cost=spell.cost,
        dmg=spell.dmg,
        heal=spell.heal,
        armor=spell.armor,
        lasts=spell.lasts,
        mana_gain=spell.mana_gain
    )


def cast(state: State, spell: Spell) -> State:
    #print(f"  cast {spell}")
    return State(
        hp=state.hp,
        mana=state.mana - spell.cost,
        armor=state.armor,
        bhp=state.bhp,
        player_turn=False,
        effects=[copy_spell(s) for s in state.effects] + [copy_spell(spell)]
    )


def least_mana_spent_to_win(hp, mana, bhp, bdmg):
    state = State(hp=hp, mana=mana, armor=0, bhp=bhp, player_turn=True, effects=[])
    q = []
    heapq.heappush(q, (0, state))
    while q:
        cost, state = heapq.heappop(q)
        #print_state(cost, state)
        apply_effects(state)
        if state.hp <= 0:
            # player dead
            #print("player dead")
            continue
        if state.bhp <= 0:
            # player won
            #print("player won")
            return cost
        if state.player_turn:
            # cast spell
            for spell in spells:
                if state.mana >= spell.cost and spell_not_active(state.effects, spell):
                    # can cast the spell
                    heapq.heappush(q, (cost + spell.cost, cast(state, spell)))
            # else: no spell was cast; that means a loss
            #       -> no push to heap
        else:
            # do damage
            atk = max(1, bdmg - state.armor)
            state.hp -= atk
            state.player_turn = True
            if state.hp > 0:
                heapq.heappush(q, (cost, state))
    assert False, "Solution not found"


def part1(input):
    setup = e.get_param()
    hp = setup.hp
    mana = setup.mana
    vals = input.get_all_ints()
    assert len(vals) == 2
    boss_hp = int(vals[0])
    boss_dmg = int(vals[1])
    return least_mana_spent_to_win(hp, mana, boss_hp, boss_dmg)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
