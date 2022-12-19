#!/usr/bin/python3.8

from aoc import Env
from dataclasses import dataclass
import re

e = Env(19)
e.T("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""",
    33, 56*62*1)

@dataclass
class Blueprint:
    # robot_material
    ore_ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int


def make_blueprints(input):
    num = re.compile(r'\d+')
    blueprints = []
    for ln in input.get_valid_lines():
        numstr = num.findall(ln)
        assert len(numstr) == 7
        nums = [int(x) for x in numstr]
        blueprints.append(Blueprint(
            ore_ore = nums[1],
            clay_ore = nums[2],
            obsidian_ore = nums[3],
            obsidian_clay = nums[4],
            geode_ore = nums[5],
            geode_obsidian = nums[6]
        ))
    return blueprints

@dataclass
class Cost:
    ore: int
    clay: int
    obsidian: int

NONE = 0
ORE = 1
CLAY = 2
OBS = 3
GEO = 4

@dataclass
class State:
    ore: int
    clay: int
    obsidian: int
    geode: int
    r_ore: int
    r_clay: int
    r_obsidian: int
    r_geode: int

    def new_robot(self, which: str, cost: Cost):
        return State(
            ore = self.ore + self.r_ore - cost.ore,
            clay = self.clay + self.r_clay - cost.clay,
            obsidian = self.obsidian + self.r_obsidian - cost.obsidian,
            geode = self.geode + self.r_geode,
            r_ore = self.r_ore + (1 if which == ORE else 0),
            r_clay = self.r_clay + (1 if which == CLAY else 0),
            r_obsidian = self.r_obsidian + (1 if which == OBS else 0),
            r_geode = self.r_geode + (1 if which == GEO else 0)
        )


def geodes_from_blueprint_0(b):
    state = State(ore=0, clay=0, obsidian=0, geode=0, r_ore=1, r_clay=0, r_obsidian=0, r_geode=0)
    states = [state]
    TIME = 24
    # stop one minute short; no point in building anything in the last minute
    for minute in range(TIME):
        print(f"minute {minute}, states {len(states)}, max geode {max([state.geode for state in states])}")

        #if (minute == 23):
        #    for state in states:
        #        if state.geode == 7:
        #            print(f"minute {minute}, state {state}")
        next_states = []
        for state in states:
            if (minute >= TIME - 2 and state.r_clay < 1) \
                or (minute >= TIME - 1 and state.r_obsidian < 1):
                # not perspective, it's too late and we don't have one
                # of the essential robots yet.
                continue
            # shortcut:
            #   if we can make a geode robot, we should
            if state.ore >= b.geode_ore and state.obsidian >= b.geode_obsidian:
                next_states.append(state.new_robot(GEO, Cost(ore=b.geode_ore, clay=0, obsidian=b.geode_obsidian)))
                continue
            if minute < TIME - 1:
                # only build other robots if there is still time for them to produce
                # resources for another geode robot
                if state.ore >= b.obsidian_ore and state.clay >= b.obsidian_clay:
                    next_states.append(state.new_robot(OBS, Cost(ore=b.obsidian_ore, clay=b.obsidian_clay, obsidian=0)))
                    continue
                if minute < TIME - 2:
                    if state.ore >= b.clay_ore and state.r_clay < 8:
                        next_states.append(state.new_robot(CLAY, Cost(ore=b.clay_ore, clay=0, obsidian=0)))
                    if minute < TIME - 3:
                        if state.ore >= b.ore_ore and state.r_ore < 7:
                            next_states.append(state.new_robot(ORE, Cost(ore=b.ore_ore, clay=0, obsidian=0)))
            # no robot produced
            next_states.append(state.new_robot(NONE, Cost(ore=0, clay=0, obsidian=0)))
        states = next_states
    ## Add r_geode to total geode once more for the last minute, which we have skipped
    #return max([state.geode + state.r_geode for state in states])
    return max([state.geode for state in states])


"""
Factory consumes resources at the beginning of the minute!
There is only 1 factory, which produces at most 1 robot at a time
"""

def min_time_to_produce_clay_robot(b: Blueprint):
    r_ore = [(1, 0)]
    min_time_clay = None
    for t in range(1, 25):
        r_ore_next = []
        for s in r_ore:
            if s[1] >= b.clay_ore:
                min_time_clay = t
                break
            if s[1] >= b.ore_ore:
                r_ore_next.append((s[0] + 1, s[1] + s[0] - b.ore_ore))
            r_ore_next.append((s[0], s[1] + s[0]))
        if min_time_clay is not None:
            break
        r_ore = r_ore_next
    return min_time_clay

def min_time_to_produce_obsidian_robot(b: Blueprint, clay_time):
    clay_robots = 1
    clay = 0
    for t in range(clay_time + 1, 25):
        clay += clay_robots
        if clay >= b.obsidian_clay:
            return t
        if t - clay_time > clay_time:
            clay_robots += 1
    return None

def min_time_to_produce_geode_robot(b, obs_time):
    obs_robots = 1
    obs = 0
    for t in range(obs_time + 1, 25):
        obs += obs_robots
        if obs >= b.geode_obsidian:
            return t
        if t - obs_time > obs_time:
            obs_robots += 1
    return None

def geodes_from_blueprint(b: Blueprint):
    # successful solution has to have at least 1 of each robot
    # start producing geodes as quickly as possible (?)
    # what's the minimal time to have an obsidian robot?

    max_ore_robots = 1
    ore = 0
    for t in range(24):
        ore += max_ore_robots
        if ore >= b.ore_ore:
            max_ore_robots += 1
            ore -= b.ore_ore
    print(f"max ore robots {max_ore_robots} with {ore} ore to spare")

    min_ore = b.geode_ore + b.obsidian_ore + b.clay_ore
    print(f"min ore required for geode robot: {min_ore}")

    # what's the minimal time to have a clay robot?
    clay_time = min_time_to_produce_clay_robot(b)
    print(f"min time to produce a clay robot: {clay_time}")

    obs_time = min_time_to_produce_obsidian_robot(b, clay_time)
    print(f"min time to produce obsidian robot +-: {obs_time}")

    geo_time = min_time_to_produce_geode_robot(b, obs_time)
    print(f"min time to produce geode robot +-: {geo_time}")

    print(f"{b.geode_ore} {b.geode_obsidian} {b.obsidian_clay} {b.clay_ore}")
    return 0



def part1(input):
    blueprints = make_blueprints(input)
    total = 0
    for i, b in enumerate(blueprints):
        geodes = geodes_from_blueprint_0(b)
        bpid = i + 1
        # Expected for the example:
        # 1: 9
        # 2: 12
        print(f"Blueprint {bpid}: {geodes} geodes")
        total += bpid * geodes
    return total


e.run_tests(1, part1)
#e.run_main(1, part1)

# 1077 too low
# 1081 correct - blueprint 4 gives 2 geodes, not 1.

def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
