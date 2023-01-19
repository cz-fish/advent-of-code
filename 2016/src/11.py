#!/usr/bin/env python3.8
import re
from collections import deque
import heapq

EXAMPLE = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""

EXPECTED = 11

MICROCHIP = 0
GENERATOR = 1

MATERIALS = []

class Thing:
    # Represent material as an index (integer) to the MATERIALS list to be able
    # to deal with numbers instead of strings
    def __init__(self, material, kind):
        dash = material.find('-')
        if dash > -1:
            material = material[:dash]

        global MATERIALS
        if material not in MATERIALS:
            MATERIALS.append(material)
        self.material = MATERIALS.index(material)
        self.kind = MICROCHIP if kind == 'microchip' else GENERATOR

    def __repr__(self):
        return f"{'M' if self.kind == MICROCHIP else 'G'}({MATERIALS[self.material]})"


def set_of_ones(val):
    c = 0
    ones = []
    while val > 0:
        if val & 1:
            ones.append(c)
        val //= 2
        c += 1
    return ones


class Floor:
    # Represent each floor as a bitmap of microchips and of generators
    # More efficient than keeping a list of things, assuming the number
    # of different materials is quite low.
    def __init__(self, chips, generators, num_things):
        self.chips = chips
        self.generators = generators
        self.num_things = num_things

    @classmethod
    def from_things(cls, things):
        chips = 0
        generators = 0
        for thing in things:
            if thing.kind == MICROCHIP:
                chips |= 2 ** thing.material
            else:
                generators |= 2 ** thing.material
        return Floor(chips, generators, len(things))

    def __repr__(self):
        def get_materials(bitmap):
            return [MATERIALS[c] for c in set_of_ones(bitmap)]
        things = [f"M({mat})" for mat in get_materials(self.chips)] + \
            [f"G({mat})" for mat in get_materials(self.generators)]
        return ', '.join(things)

    def empty(self):
        return self.chips == 0 and self.generators == 0

    def get_one_or_two_things(self):
        # yield (picked_microchips, picked_generators, new_floor_after_picking)
        # only if new_floor_after_picking is valid
        chips = set_of_ones(self.chips)
        gens = set_of_ones(self.generators)

        def all_options():
            # pick one or two chips
            for i in range(len(chips)):
                first = 2 ** chips[i]
                yield (first, 0, 1)
                for j in range(i+1, len(chips)):
                    second = 2 ** chips[j]
                    yield (first | second, 0, 2)

            # pick one or two generators
            for i in range(len(gens)):
                first = 2 ** gens[i]
                yield (0, first, 1)
                for j in range(i+1, len(gens)):
                    second = 2 ** gens[j]
                    yield (0, first | second, 2)

            # pick one chip and one generator
            for i in chips:
                for j in gens:
                    yield (2**i, 2**j, 2)

        chip_and_its_gen = False
        for opt_chip, opt_gen, num_things in all_options():

            if opt_chip !=0 and opt_gen != 0 and opt_chip & opt_gen == opt_chip:
                # [this optimization reduced states from 2.7M to 2.15M in part 2]
                # we're picking a chip and its generator
                # If there are multiple different pairs of chips and their own
                # generators on the same floor, we don't need to try all the options,
                # just one of them. The solution will be equivalent, no matter what
                # material and chip do we pick
                if chip_and_its_gen:
                    continue
                chip_and_its_gen = True

            new_floor = self.withoutThings(opt_chip, opt_gen, num_things)
            if new_floor.is_valid():
                yield (opt_chip, opt_gen, new_floor, num_things)

    def withExtraThings(self, add_chips, add_generators, num_things):
        return Floor(self.chips | add_chips, self.generators | add_generators, self.num_things + num_things)
    
    def withoutThings(self, remove_chips, remove_generators, num_things):
        return Floor(self.chips & ~remove_chips, self.generators & ~remove_generators, self.num_things - num_things)

    def is_valid(self):
        # floor is valid if 
        # a) there are no generators
        if self.generators == 0:
            return True
        # or b) each chip present has its generator also present
        return self.chips & self.generators == self.chips

    def __lt__(self, other):
        # Make two Floor instances comparable to make the heapq happy, but otherwise
        # there isn't any particular reason for this ordering.
        return (self.chips, self.generators) < (other.chips, other.generators)


class HashKey:
    def __init__(self, current, floors):
        values = [current]
        values += [fl.chips for fl in floors]
        values += [fl.generators for fl in floors]
        self.values = tuple(values)

    def __hash__(self):
        return hash(self.values)
    
    def __eq__(self, other):
        return other and self.values == other.values
    
    def __ne__(self, other):
        return not (self == other)


def parse_input(lines):
    assert len(lines) == 4
    pat = re.compile(r'([^ ]+) (microchip|generator)')
    floors = []
    for ln in lines:
        things = pat.findall(ln)
        floors.append(Floor.from_things([Thing(mat, kind) for mat, kind in things]))
    return floors


def end_state(current, floors):
    return current == 3 and floors[0].empty() and floors[1].empty() and floors[2].empty()


def heuristic(current, floors):
    # Lower bound (underestimated) number of steps necessary to bring all items from the given
    # configuration to the fourth floor
    lowest_nonempty_floor = 3
    cost = 0
    for i in range(3):
        items = floors[i].num_things
        if items > 0:
            if i < lowest_nonempty_floor:
                lowest_nonempty_floor = i
                if current > i:
                    # we will still have to go down from current to 'i' to pick up what's there
                    cost += current - i
            if i != current:
                # [reduced number of states from 2.15M to 1.55M in part 2]
                # When we go to this floor, we will be carrying at least one additional item with us
                items += 1

            # To pick up all items, we need to visit the floor at least items -1 times
            # After each visit, when there are any items left, we still need to return to the
            # floor, which is one extra step for each additional item over 2
            steps_up = max(1, items - 1)
            steps_down = max(0, items - 2)
            # All the way to the fourth floor
            cost += (3 - i) * (steps_up + steps_down)
    return cost


# BFS, ~158000 states visited in part 1
def min_steps_to_4_bfs(floors):
    q = deque()
    q.append((0, 0, floors))
    visited = set()
    while q:
        steps, current, floors = q.popleft()
        if end_state(current, floors):
            print(f"States visited: {len(visited)}")
            return steps
        key = HashKey(current, floors)
        if key in visited:
            continue
        visited.add(key)
        # try picking one or two items from the current floor
        for pick_chip, pick_gener, new_source_floor, num_things in floors[current].get_one_or_two_things():
            # try to go 1 floor up or down
            for change in [1, -1]:
                new_floor_nr = current + change
                if new_floor_nr < 0 or new_floor_nr >= 4:
                    # out of bounds
                    continue
                new_dest_floor = floors[new_floor_nr].withExtraThings(pick_chip, pick_gener, num_things)
                if not new_dest_floor.is_valid():
                    # movin stuff to the new floor would make it imbalanced
                    continue
                # move is valid
                new_floors = floors[:]
                new_floors[current] = new_source_floor
                new_floors[new_floor_nr] = new_dest_floor
                q.append((steps + 1, new_floor_nr, new_floors))
    assert False, "solution not found"

# A*, ~31k states visited in part 1, 3.3M states visited in part 2
def min_steps_to_4(floors):
    q = []
    print(f"Initial state cost from heuristic: {heuristic(0, floors)}")
    heapq.heappush(q, (heuristic(0, floors), 0, 0, floors))
    visited = set()
    while q:
        _, steps, current, floors = heapq.heappop(q)
        if end_state(current, floors):
            print(f"States visited: {len(visited)}")
            return steps
        key = HashKey(current, floors)
        if key in visited:
            continue
        visited.add(key)
        # try picking one or two items from the current floor
        for pick_chip, pick_gener, new_source_floor, num_things in floors[current].get_one_or_two_things():
            # try to go 1 floor up or down
            for change in [1, -1]:

                # [with this optimization, down from 3.3M to 2.7M states in part 2]:
                # does it ever make sense to just carry down 2 microchips?
                if change == -1 and pick_gener == 0 and num_things == 2:
                    continue

                new_floor_nr = current + change
                if new_floor_nr < 0 or new_floor_nr >= 4:
                    # out of bounds
                    continue
                new_dest_floor = floors[new_floor_nr].withExtraThings(pick_chip, pick_gener, num_things)
                if not new_dest_floor.is_valid():
                    # movin stuff to the new floor would make it imbalanced
                    continue
                # move is valid
                new_floors = floors[:]
                new_floors[current] = new_source_floor
                new_floors[new_floor_nr] = new_dest_floor
                heapq.heappush(q, (steps + 1 + heuristic(new_floor_nr, new_floors), steps + 1, new_floor_nr, new_floors))
    assert False, "solution not found"


def solve(floors):
    for i, floor in enumerate(floors):
        print(f"{i+1}: {floor}")

    return min_steps_to_4(floors)


if __name__ == "__main__":
    # Test for part 1
    test_floors = parse_input(EXAMPLE.split('\n'))
    test_value = solve(test_floors)
    print(f"Test result: {test_value}")
    assert test_value == EXPECTED, f"Test expected {EXPECTED}, got {test_value}"
    print()

    # clear global state (sic)
    MATERIALS = []

    # Actual part 1
    with open('../input11.txt', 'rt') as f:
        actual_input = f.readlines()
    floors_pt1 = parse_input(actual_input)
    part1 = solve(floors_pt1)
    print(f"Part 1: {part1}")
    print()

    # Actual part 2
    floors_pt2 = parse_input(actual_input)
    extra_things = [
        Thing('elerium', 'generator'),
        Thing('elerium-compatible', 'microchip'),
        Thing('dilithium', 'generator'),
        Thing('dilithium-compatible', 'microchip')
    ]
    dummy_floor = Floor.from_things(extra_things)
    floors_pt2[0] = floors_pt2[0].withExtraThings(dummy_floor.chips, dummy_floor.generators, dummy_floor.num_things)
    part2 = solve(floors_pt2)
    print(f"Part 2: {part2}")
