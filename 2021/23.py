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


### --- INPUT PARSING ---
# The part 1 state consists of 8 + 11 positions. The first 8 positions are the pits where
# the amphipods start (and finish) and 11 positions are the corridor.

def parse_input(input):
    """
.............
.89ABCDEFXYZ.
...0.2.4.6...
  .1.3.5.7.
  .........
"""
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


# This turns parsed part 1 input into input suitable for part 2 algorithm. The part 2 algo
# assumes that each pit is 4 positions long, which was not the case in part 1. So to be able
# to solve both part 1 and part 2 with the same function without modifications, in case of
# part 1 we pad the bottom two rows of each pit with the correct amphipod - so that the pits
# are of length 4, but the bottom 2 amphipods will never move.

def make_pt2_compatible_input(pt1_state, is_for_pt1):
    """
.............
.8 ~~~~~~ 18.
...0.2.4.6...
  .1.3.5.7.
  .........

to

.............
.16 ~~~~~ 26.
...3.7.B.F...
  .2.6.A.E.
  .1.5.9.D.
  .0.4.8.C.
  .........

pt2: insert
  .D.C.B.A.
  .D.B.A.C.
between 2 lines
"""
    def p1p2(x):
        col = x // 2
        row = x % 2
        return 4 * col + 3 - row
    
    def p2p2(x):
        col = x // 2
        row = x % 2
        return 4 * col + 3 * (1 - row)

    i = pt1_state
    if is_for_pt1:
        # part1: fill bottom 2 lines with ABCD
        return [
            p1p2(i[0]), p1p2(i[1]), 1, 0,  # A
            p1p2(i[2]), p1p2(i[3]), 5, 4,  # B
            p1p2(i[4]), p1p2(i[5]), 9, 8,  # C
            p1p2(i[6]), p1p2(i[7]), 13, 12 # D
        ]
    else:
        # part2: insert DCBA, DBAC in the middle
        return [
            p2p2(i[0]), p2p2(i[1]), 14, 9,  # A
            p2p2(i[2]), p2p2(i[3]), 10, 5,  # B
            p2p2(i[4]), p2p2(i[5]), 6, 13,  # C
            p2p2(i[6]), p2p2(i[7]), 2, 1    # D
        ]


### --- ORIGINAL PART 1 SOLUTION ---
# (works but is very slow)
# we move the amphipods through all possible moves, and maintain a priority queue of states, sorted
# by the cost (in energy) of each state, from lowest to highest. This is slow because steps of
# amphipod D are 1000x more expensive and therefore we explore way too many useless combinations
# of steps of A, B, C before we get to D. On the other hand, the first solution that we find is
# guaranteed to be minimal.
# If we visit a state that we've seen before (the 's' set), then we just ignore it, because we know
# that the current cost is worse than the previous cost when we visited the same state. This is
# a helpful pruning optimization.

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


### --- FASTER PART 2 SOLUTION ---
# (also applicable to part 1)
# lots of copy/paste from the above original solution, but with hardcoded 2 and 8 replaced by some named constants.
# The main difference is that the algo doesn't search all states in the order of minimal cost, but it does a sort
# of depth-first-search. That is not guaranteed to find the minimal solution, but it finds some solution. Then all
# states left in the heap that have cost bigger than the current best solution can be pruned. When we find a cheaper
# solution, we update the best, and this continues until all branches have been tried.
# We also prune the branches where we end up in the same state that we have seen before, but only if the current cost
# is worse than that of the previous visit, because that's not guaranteed.

CT = 4
PITS = 16

def is_final_state_pt2(state):
    return all([i // CT == x // CT for i, x in enumerate(state)])


def in_correct_pit(char, pos, pos_map):
    col = pos // CT
    row = pos % CT
    if col != char:
        # wrong pit altogether
        return False
    for i in range(1, row+1):
        if pos_map[pos - i] != char:
            # something underneath char in the current col is of the wrong type
            return False
    return True


def at_top_of_pit(pos, pos_map):
    col = pos // CT
    row = pos % CT
    for i in range(row + 1, CT):
        if col * CT + i in pos_map:
            return False
    return True


def get_top_of_pit(pit, pos_map):
    for i in range(CT):
        pos = pit * CT + i
        if pos not in pos_map:
            return pos
        if pos_map[pos] != pit:
            # some wrong char in the pit
            return None
    # pit full. This probably can't be reached
    return None


def path_steps_pt2(f, t, pos_map):
    """Count steps between position f and t. Return None if the path is blocked.
       Only valid for movement between pit and corridor; not valid to move from pit to pit or from corridor to corridor"""
    if t in pos_map:
        # destination occuppied
        return None
    pit_pos = min(f, t)
    cor_pos = max(f, t)
    assert pit_pos < PITS and cor_pos >= PITS, f"Movement pit->pit or corridor->corridor is not allowed ({f}, {t}, {pit_pos}, {cor_pos})"
    col = pit_pos // CT
    row = pit_pos % CT
    x = PITS + 2 + 2 * col
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
    dist_in_pit = CT - 1 - row
    dist_in_corridor = r[1] - r[0] + 1
    return dist_in_pit + dist_in_corridor


def append_dest_if_path_free_pt2(f, t, destinations, pos_map):
    steps = path_steps_pt2(f, t, pos_map)
    if steps is not None:
        destinations.append((t, steps))


def print_state_pt2(state):
    g = [['#' for _ in range(13)] for _ in range(7)]
    for i in range(1, 12):
        g[1][i] = '.'
    for i in [3,5,7,9]:
        for j in range(2, 6):
            g[j][i] = '.'
    for i in [0, 1, -1, -2]:
        for j in range(3, 7):
            g[j][i] = ' '
    for i, v in enumerate(state):
        char = chr(i // 4 + ord('A'))
        if v < 16:
            col = v // 4
            row = 3 - v % 4
            g[row + 2][2*col+3] = char
        else:
            g[1][v - 16 + 1] = char
    for ln in g:
        print(''.join(ln))


def strstate(state):
    s = ['.' for _ in range(27)]
    for i, e in enumerate(state):
        c = chr(i // CT + ord('A'))
        s[e] = c
    return ''.join(s)


def find_min_cost_pt2(state):
    h = []
    heapq.heappush(h, (0, state, 0))
    best = None
    #counter = 0
    s = {}

    while h:
        steps, state, cost = heapq.heappop(h)
        #counter += 1
        if best is not None and cost >= best:
            continue
        if is_final_state_pt2(state):
            best = cost
            #print(f"counter {counter}, best {best}")
            continue

        #if counter % 100000 == 0:
        #    print(counter, best, len(h))

        uniqkey = strstate(state)
        if uniqkey in s and s[uniqkey] <= cost:
           continue
        s[uniqkey] = cost

        pos_map = {
            v: i // CT for i, v in enumerate(state)
        }

        for pick in range(CT * 4):
            char = pick // CT
            pos = state[pick]
            dests = []
            if pos < PITS:
                # char currently in pit, move to corridor
                if in_correct_pit(char, pos, pos_map):
                    # char already in the correct pit and everything under it is sorted
                    continue
                if not at_top_of_pit(pos, pos_map):
                    # some other char is above in the same pit - cannot move
                    continue
                # move from pit to corridor
                for cor in [0, 1, 3, 5, 7, 9, 10]:
                    cor += PITS
                    append_dest_if_path_free_pt2(pos, cor, dests, pos_map)

            else:
                # char currently in corridor, move to pit
                top_of_pit = get_top_of_pit(char, pos_map)
                if top_of_pit is None:
                    # something wrong is currently in the pit, cannot jump there
                    continue
                append_dest_if_path_free_pt2(pos, top_of_pit, dests, pos_map)

            for new_pos, new_steps in dests:
                add_cost = new_steps * (10**char)
                new_state = state[:]
                new_state[pick] = new_pos
                new_cost = cost + add_cost
                t = strstate(new_state)
                if t not in s or s[t] > new_cost:
                    heapq.heappush(h, (steps - 100000 + add_cost, new_state, new_cost))

    assert best is not None, "Didn't find a solution"
    return best



def part1(input):
    state = parse_input(input)
    bigstate = make_pt2_compatible_input(state, True)
    # print_state_pt2(bigstate)
    return find_min_cost_pt2(bigstate)
    # return find_min_cost(state)  # the old slow implementation


assert in_correct_pit(0, 3, {3:0, 2:0, 1:0, 0:0})
assert in_correct_pit(0, 2, {2:0, 1:0, 0:0})
assert in_correct_pit(1, 5, {5:1, 4:1, 0:0})
assert not in_correct_pit(0, 7, {7:0, 6:1, 5:1, 4:1})
assert not in_correct_pit(0, 3, {3:0, 2:0, 1:1, 0:0})

assert at_top_of_pit(3, {3:0, 2:0, 1:0, 0:0})
assert not at_top_of_pit(2, {3:0, 2:0, 1:0, 0:0})
assert not at_top_of_pit(1, {3:0, 2:0, 1:0, 0:0})
assert not at_top_of_pit(0, {3:0, 2:0, 1:0, 0:0})
assert at_top_of_pit(5, {3:0, 2:0, 1:0, 0:0, 5:1, 4:2})
assert at_top_of_pit(2, {2:0, 1:0, 0:0})
assert not at_top_of_pit(1, {2:0, 1:0, 0:0})
assert not at_top_of_pit(0, {2:0, 1:0, 0:0})
assert at_top_of_pit(1, {1:0, 0:0})

assert get_top_of_pit(3, {0:0, 12:1, 13:2, 14:0, 15:1}) is None
assert get_top_of_pit(3, {0:0, 12:1, 13:2, 14:0}) is None
assert get_top_of_pit(3, {0:0, 12:3, 13:3, 14:3}) == 15
assert get_top_of_pit(2, {0:0, 12:1, 13:2, 14:0}) == 8
assert get_top_of_pit(1, {0:0, 12:1, 13:2, 14:0}) == 4
assert get_top_of_pit(0, {0:0, 12:1, 13:2, 14:0}) == 1

assert not in_correct_pit(1, 5, {0:0, 1:3, 2:3, 3:1, 4:3, 5:1})
assert at_top_of_pit(5, {0:0, 1:3, 2:3, 3:1, 4:3, 5:1})

print("sanity tests passed")


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    state = parse_input(input)
    bigstate = make_pt2_compatible_input(state, False)
    # print_state_pt2(bigstate)
    return find_min_cost_pt2(bigstate)


e.run_tests(2, part2)
e.run_main(2, part2)
