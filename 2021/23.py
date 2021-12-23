#!/usr/bin/python3.8

from aoc import Env
import heapq

e = Env(23)
e.T("""#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #########""", 46, None)

e.T("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""", 12521, 44169)


def parse_input(input):
    lines = input.get_valid_lines()
    assert len(lines) == 5
    a = lines[2].strip()
    b = lines[3].strip()
    p = a[3] + b[1] + a[5] + b[3] + a[7] + b[5] + a[9] + b[7]
    assert all([x in 'ABCD' for x in p])
    pos = [-1 for _ in range(8)]
    for i, x in enumerate(p):
        char = ord(x) - ord('A')
        if pos[2 * char] == -1:
            pos[2 * char] = i
        else:
            assert pos[2 * char + 1] == -1
            pos[2 * char + 1] = i
    return pos

"""
.............
.89ABCDEFXYZ.
...0.2.4.6...
  .1.3.5.7.
  .........
"""

def is_final_state(state):
    return state[0] in [0,1] and state[1] in [0,1] and state[2] in [2,3] and state[3] in [2,3] and \
           state[4] in [4,5] and state[5] in [4,5] and state[6] in [6,7] and state[7] in [6,7]


def path_steps(f, t, pos_map):
    """Count steps between position f and t. Return None if the path is blocked.
       Only valid for movement between pit and corridor; not valid to move from pit to pit or from corridor to corridor"""
    if t in pos_map:
        # destination occuppied
        return None
    pit_pos = min(f, t)
    cor_pos = max(f, t)
    assert pit_pos < 8 and cor_pos >= 8, "Movement pit->pit or corridor->corridor is not allowed"
    x = 10 + (pit_pos // 2) * 2
    assert cor_pos != x, f"Trying to go to corridor position just above a pit ({f}, {t}, {pit_pos}, {cor_pos}, {x})"
    if cor_pos < x:
        # leave pit and go left
        r = (cor_pos, x)
    else:
        # leave pit and go right
        r = (x, cor_pos)
    if any([x in pos_map for x in range(r[0], r[1]+1) if x != f]):
        # path blocked
        return None
    # number of steps to go to the position
    dist_in_pit = pit_pos % 2
    dist_in_corridor = r[1] - r[0] + 1
    return dist_in_pit + dist_in_corridor


def append_dest_if_path_free(f, t, destinations, pos_map):
    steps = path_steps(f, t, pos_map)
    if steps is not None:
        destinations.append((t, steps))


def find_min_cost(state):
    counter = 0
    h = []
    heapq.heappush(h, (0, state))
    s = set()
    while h:
        cost, state = heapq.heappop(h)
        s.add(tuple(state))
        counter += 1
        if counter % 1000000 == 0:
            print(counter, cost, state)
        #print(cost, state)
        if is_final_state(state):
            return cost
        
        pos_map = {
            v: i // 2 for i, v in enumerate(state)
        }

        for pick in range(8):
            char = pick // 2
            pos = state[pick]
            dests = []
            if pos == 2 * char + 1:
                # char already at the bottom of the right pit
                continue
            if pos == 2 * char and pos_map[2 * char + 1] == char:
                # char at the top of the right pit, and the one below is the correct one also
                continue
            if pos < 8:
                # in a pit
                if pos % 2 == 1 and pos - 1 in pos_map:
                    # at the bottom, and there is something at the top of the same pit. Cannot move
                    continue
                # move from pit to corridor
                for cor in [8,9,11,13,15,17,18]:
                    append_dest_if_path_free(pos, cor, dests, pos_map)
            else:
                # in the corridor, move to the pit
                pit = char * 2
                if pit in pos_map:
                    # something is at the top of the destination pit
                    continue
                if pit + 1 in pos_map:
                    # something is at the bottom of the destination pit
                    if pos_map[pit+1] == char:
                        # it's the right thing, we can move on top of it
                        append_dest_if_path_free(pos, pit, dests, pos_map)
                else:
                    # pit is empty
                    append_dest_if_path_free(pos, pit + 1, dests, pos_map)

            for cor, steps in dests:
                add_cost = steps * 10**char
                new_state = state[:]
                new_state[pick] = cor

                t = tuple(new_state)
                if t in s:
                    continue

                #print(f"{cost}: {state} {chr(char + ord('A'))} can go from {pos} to {cor} for {add_cost} cost")
                #print (cost + add_cost, new_state)
                heapq.heappush(h, (cost + add_cost, new_state))
    else:
        assert False, "Couldn't find an end state"


def part1(input):
    state = parse_input(input)
    return find_min_cost(state)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    pass


# e.run_tests(2, part2)
# e.run_main(2, part2)
