#!/usr/bin/python3.8

from aoc import Env

e = Env(7)
e.T("16,1,2,0,4,2,7,1,2,14", 37, 168)
e.T("1,1,16", 15, 85)


def cost_pt1(crabs, pos):
    return sum([abs(pos - crab) for crab in crabs])


def cost_pt2(crabs, pos):
    return sum([
        abs(pos - crab) * (abs(pos - crab) + 1)//2
        for crab in crabs
    ])


def bruteforce(crabs, cost):
    m = min(crabs)
    M = max(crabs)
    best = None
    bestpos = None
    for x in range(m, M+1):
        c = cost(crabs, x)
        if best is None or c < best:
            best = c
            bestpos = x
    return best


def part1(input):
    crabs = sorted(input.get_all_ints())
    
    # return bruteforce(crabs, cost_pt1)
    
    # Let's choose some position X. Then A crabs are to the left
    # of X, and B crabs to the right. If we were to move X one position
    # to the left (X-1), the total cost would decrease by A, and
    # increase by B. Analogically for moving right (X+1).
    # The optimal position is therefore one where we have the same
    # number on the left as on the right, A=B.
    #
    # Therefore pick the median.
    med = crabs[len(crabs)//2]
    return min(cost_pt1(crabs, med), cost_pt1(crabs, med+1))


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    crabs = sorted(input.get_all_ints())

    # return bruteforce(crabs, cost_pt2)

    # In this case, we're picking the average of the positions
    # to minimize the sum of distances of all crabs from the point.
    # If we moved the point to either side from the average position
    # the increase of fuel on one side would be higher than the
    # decrease on the other side.
    avg = sum(crabs)//len(crabs)
    return min(cost_pt2(crabs, avg), cost_pt2(crabs, avg+1))


e.run_tests(2, part2)
e.run_main(2, part2)
