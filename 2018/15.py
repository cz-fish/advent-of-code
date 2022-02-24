#!/usr/bin/python3.8

from aoc import Env, Grid
#from collections import Namedtuple
from collections import deque

def eT(*a):
    pass

e = Env(15)
e.T("""#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""", 27730, 4988) # attack 15
e.T("""#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""", 36334, None)
e.T("""#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""", 39514, 31284) # attack 4
e.T("""#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""", 27755, 3478) # attack 15
e.T("""#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""", 28944, 6474) # attack 12
e.T("""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""", 18740, 1140) # attack 34


START_HP = 200
START_ATK = 3
MAX_COLS = 100


class Unit:
    def __init__(self, type, pos, attack):
        self.elf = type == 'E'
        self.pos = pos
        self.hp = START_HP
        self.atk = attack

    def __repr__(self):
        return '[{} {} {}]'.format('GE'[self.elf], self.pos, self.hp)


Goblin = 0
Elf = 1


def initial_units(grid, elf_attack=START_ATK):
    assert grid.w < MAX_COLS
    units = []
    for row in range(grid.h):
        for col in range(grid.w):
            c = grid.get(row, col)
            if c in 'GE':
                if c == 'E':
                    attack = elf_attack
                else:
                    attack = START_ATK
                u = Unit(c, (row, col), attack)
                units.append(u)
    return units


def reading_order(lst):
    return sorted(lst, key=lambda u: u.pos[0] * MAX_COLS + u.pos[1])


def collect_units(units):
    return [u for u in units if u.hp > 0]

def reading_order_offsets(base_pos):
    return [(base_pos[0]-1, base_pos[1]), (base_pos[0], base_pos[1]-1), (base_pos[0], base_pos[1]+1), (base_pos[0]+1, base_pos[1])]

def grid_neighbors_in_reading_order(grid, y, x):
    # The order of neighbors is actually the same as in the neighbor4 method. But I want to be
    # explicit, because the order is important here.
    return grid._neighborCoords(y, x, False, False, reading_order_offsets((0, 0)))

def find_move(unit, grid):
    # Returns new position after the move, and True if already in range and can attack
    other = 'EG'[unit.elf]
    x = unit.pos[1]
    y = unit.pos[0]
    for r, c in grid.neighbors4(y, x):
        if grid.get(r, c) == other:
            # Already in range of an enemy - don't move
            return y, x, True

    # BFS in the reading order - up, left, right, down    
    q = deque()
    seen = set()
    for nei in grid_neighbors_in_reading_order(grid, y, x):
        if grid.get(nei[0], nei[1]) == '.':
            q.append((nei[0], nei[1], (nei[0], nei[1])))
    while q:
        r, c, first_step = q.popleft()
        if (r, c) in seen:
            continue
        #if first_step is None:
        #    # This is the first step of the path
        #    first_step = (r, c)
        seen.add((r, c))
        # The order of neighbors is actually the same as in the neighbor4 method. But I want to be
        # explicit, because the order is important here.
        for nei in grid_neighbors_in_reading_order(grid, r, c):
            what = grid.get(nei[0], nei[1])
            if what == other:
                # Found an enemy at coords 'nei', which means that '(r, c)' is in range.
                # Because we used BFS, it is (one of the) nearest positions in range.
                # Because the BFS was in reading order, this is the first in range in reading order.
                # We can't move directly to the position, but we make the first step.
                return first_step[0], first_step[1], (r, c) == first_step
            elif what == '.':
                q.append((nei[0], nei[1], first_step))

    # we didn't find any reachable position in range. No move
    return y, x, False


def round(grid, units):
    units = reading_order(units)
    enemy = [{}, {}]
    for u in units:
        enemy[not u.elf][f"{u.pos[0]},{u.pos[1]}"] = u
    elf_died = False

    # for each unit in the initial order
    for u in units:
        if u.hp <= 0:
            # unit already killed
            continue

        if not enemy[u.elf]:
            # no enemies left
            return True, collect_units(units), elf_died

        # Move the unit
        move_r, move_c, can_attack = find_move(u, grid)
        grid.grid[u.pos[0]][u.pos[1]] = '.'
        del enemy[not u.elf][f"{u.pos[0]},{u.pos[1]}"]
        grid.grid[move_r][move_c] = 'GE'[u.elf]
        u.pos = (move_r, move_c)
        enemy[not u.elf][f"{u.pos[0]},{u.pos[1]}"] = u

        if not can_attack:
            continue

        eType = 'EG'[u.elf]
        leastHpUnit = None
        leastUnitPos = None
        for around in reading_order_offsets(u.pos):
            if grid.get(around[0], around[1]) == eType:
                pos = f"{around[0]},{around[1]}"
                assert pos in enemy[u.elf]
                eUnit = enemy[u.elf][pos]
                if leastHpUnit is None or leastHpUnit.hp > eUnit.hp:
                    leastHpUnit = eUnit
                    leastUnitPos = pos
        assert leastHpUnit is not None, "Enemy was supposed to be in range, but none found"

        leastHpUnit.hp -= u.atk
        if leastHpUnit.hp <= 0:
            if leastHpUnit.elf:
                elf_died = True
            del enemy[u.elf][leastUnitPos]
            grid.grid[leastHpUnit.pos[0]][leastHpUnit.pos[1]] = '.'

    # All units moved and the game didn't end yet
    return False, collect_units(units), elf_died


def print_state(grid, units):
    for row in grid.grid:
        print(''.join(row))
    print("----")
    for u in units:
        print(u)
    print("\n\n")


def get_outcome(round_nr, units):
    return round_nr * sum([u.hp for u in units if u.hp > 0])


def part1(input):
    g = Grid(input.get_valid_lines())
    units = initial_units(g)
    round_nr = 0
    # print_state(g, units)
    while True:
        finished, units, _ = round(g, units)
        if finished:
            break
        round_nr += 1
    # print(f"final: round {round_nr}, remaining {sum([u.hp for u in units if u.hp > 0])}")
    # print_state(g, units)
    return get_outcome(round_nr, units)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    elf_attack = START_ATK
    while True:
        g = Grid(input.get_valid_lines())
        units = initial_units(g, elf_attack)
        round_nr = 0
        while True:
            finished, units, elf_died = round(g, units)
            if finished or elf_died:
                break
            round_nr += 1
        if elf_died:
            elf_attack += 1
        else:
            return get_outcome(round_nr, units)


e.run_tests(2, part2)
e.run_main(2, part2)
