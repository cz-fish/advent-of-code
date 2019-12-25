#!/usr/bin/env python3

import intcode
import sys
from collections import namedtuple

Room = namedtuple('Room', ['name', 'desc', 'directions', 'items', 'path'])

with open('input25.txt', 'rt') as f:
    lines = f.readline().strip()

program = [int(i) for i in lines.split(',')]

plan = {}
path = ''
current = None
screen = ''
tried = {}
input = ''
inputpos = 0
phase = 1
all_items = {}
weights = {}
carried_items = ''
checkpoint = 'Security Checkpoint'
sensitive_floor = 'Pressure-Sensitive Floor'
item_combos = []
current_combo = 0


def do_weighting(lines):
    for ln in lines:
        if ln.startswith('A loud, robotic'):
            if 'are heavier' in ln:
                weight = 'light'
            elif 'are lighter' in ln:
                weight = 'heavy'
            else:
                print(lines)
                sys.exit(0)
    print(f'Items: {carried_items}, result: {weight}')
    global weights
    weights[carried_items] = weight


def parse_screen(screen):
    global plan
    global current
    directions = []
    items = []
    lines = screen.split('\n')
    room = None
    for i, ln in enumerate(lines):
        if ln.startswith('You take the'):
            # for x in lines:
            #     if x:
            #         print(x)
            return
        if ln.startswith('You drop the'):
            return

        if ln.startswith('== '):
            room = ln[3:-3]
            if room == sensitive_floor:
                do_weighting(lines)
                return
            current = room
            if room in plan:
                # we've already been here
                return
            desc = lines[i+1]
        elif ln.startswith('Doors here lead:'):
            for j in range(1, 5):
                if lines[i + j].startswith('- '):
                    directions += [lines[i+j][2:]]
                else:
                    break
        elif ln.startswith('Items here:'):
            j = 1
            while True:
                if lines[i+j].startswith('- '):
                    items += [lines[i+j][2:]]
                else:
                    break
                j += 1
    global path
    if room is None:
        print(lines)
        sys.exit(0)
    plan[room] = Room(name=room, desc='', directions=directions, items=items, path=path)
    print(plan[room])


def reverse_dir(d):
    return {
        'N': 'south',
        'E': 'west',
        'S': 'north',
        'W': 'east'
    }[d]


def command_to_dir(cmd):
    return {
        'north': 'N',
        'east': 'E',
        'south': 'S',
        'west': 'W'
    }[cmd]


def dir_to_command(d):
    return {
        'N': 'north',
        'E': 'east',
        'S': 'south',
        'W': 'west'
    }[d]


def phase1_exploration():
    global path

    room = plan[current]
    name = room.name

    last_command = None
    came_from = None
    if path:
        last_command = path[-1]
        came_from = reverse_dir(last_command)

    if name not in tried:
        tried[name] = set()
    tried[name].add(came_from)

    dirs_to_try = set(room.directions) - tried[name]

    if not dirs_to_try or name == checkpoint:
        # already tried all directions from room
        if not came_from:
            # we're back at start and we've explored everything
            print('End of exploration, all rooms discovered')
            return None
        path = path[:-1]
        # go back one room
        return came_from

    take = list(dirs_to_try)[0]
    tried[name].add(take)
    path += command_to_dir(take)
    return take


def init_phase2():
    global all_items
    for name, room in plan.items():
        for item in room.items:
            all_items[item] = room.path
    del all_items['giant electromagnet']
    del all_items['infinite loop']
    del all_items['photons']
    del all_items['molten lava']
    del all_items['escape pod']


def go_path(path):
    return [dir_to_command(d) for d in path]


def go_back(path):
    return [reverse_dir(d) for d in path[::-1]]


def phase2_weighting():
    global carried_items
    remaining_items = set(all_items.keys()) - set(weights.keys())
    if not remaining_items:
        print('End of weighting, all items weighted and returned')
        return None
    item = list(remaining_items)[0]
    path_to_item = all_items[item]
    path_to_checkpoint = plan[checkpoint].path
    carried_items = item

    commands = go_path(path_to_item) + \
        [f'take {item}'] + \
        go_back(path_to_item) + \
        go_path(path_to_checkpoint) + \
        ['west'] + \
        go_back(path_to_checkpoint) + \
        go_path(path_to_item) + \
        [f'drop {item}'] + \
        go_back(path_to_item)

    # print(commands)
    return '\n'.join(commands)


def init_phase3():
    global item_combos
    eligible_items = [item for item in weights.keys() if weights[item] == 'light']
    ll = len(eligible_items)
    print(f'{ll} eligible items: {str(eligible_items)}')
    for i in range(2 ** ll):
        # only combos with 2 or more items
        bits = bin(i).count('1')
        if bits < 2:
            continue
        combo = []
        for j in range(ll):
            if i & (2 ** j):
                combo += [eligible_items[j]]
        item_combos += [combo]
    print(f'Item combos: {len(item_combos)}')
    #for c in item_combos:
    #    print(c)


def phase3_take():
    global item_combos
    global current_combo

    if current_combo >= len(item_combos):
        print('All item combos tried')
        sys.exit(0)
        return None

    combo = item_combos[current_combo]
    current_combo += 1

    print('Combo:', combo)
    commands = []
    for item in combo:
        commands += go_path(all_items[item]) + \
            [f'take {item}'] + \
            go_back(all_items[item])
    commands += go_path(plan[checkpoint].path) + \
        ['west'] + \
        go_back(plan[checkpoint].path)
    for item in combo:
        commands += go_path(all_items[item]) + \
            [f'drop {item}'] + \
            go_back(all_items[item])

    global carried_items
    carried_items = ','.join(combo)
    return '\n'.join(commands)


def get_next_input():
    global phase
    if phase == 1:
        res = phase1_exploration()
        if res is not None:
            return res
        phase = 2
        init_phase2()
    if phase == 2:
        res = phase2_weighting()
        if res is not None:
            return res
        phase = 3
        init_phase3()
    if phase == 3:
        res = phase3_take()
        return res


def input_fn():
    global inputpos
    global input
    global current
    if inputpos >= len(input):
        input = [ord(c) for c in get_next_input() + '\n']
        inputpos = 0
    v = input[inputpos]
    inputpos += 1
    return v


def output_fn(val):
    global screen
    #if phase == 2:
    #    print(chr(val), end='')
    screen += chr(val)
    if len(screen) > 8 and screen.endswith('Command?'):
        parse_screen(screen)
        screen = ''


mach = intcode.IntCode(program)
mach.run(input_fn, output_fn)

parse_screen(screen)
