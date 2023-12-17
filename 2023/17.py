#!/usr/bin/python3.8

from aoc import Env, Grid
import heapq
from collections import defaultdict

e = Env(17)
e.T("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""", 102, 94)

e.T("""111111111111
999999999991
999999999991
999999999991
999999999991""", None, 71)


RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
STEP = {
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1),
    UP: (-1, 0),
}


def one_step_in_direction(row, col, head):
    return (row + STEP[head][0], col + STEP[head][1], head)


def min_heat_loss(grid, start, end):
    # (heuristic_key, loss_so_far, row, column, heading, steps_in_current_dir)
    q = [(0, 0, start[0], start[1], RIGHT, 0)]
    tried = {}
    while q:
        _, loss, row, col, head, steps = heapq.heappop(q)
        if (row, col) == end:
            return loss
        follow = []
        if steps < 3:
            # forward
            follow.append((one_step_in_direction(row, col, head), steps + 1))
        # left
        follow.append((one_step_in_direction(row, col, (head - 1) % 4), 1))
        # right
        follow.append((one_step_in_direction(row, col, (head + 1) % 4), 1))
        for pos, nsteps in follow:
            nr, nc, nhead = pos
            if not grid.is_in(nr, nc):
                continue
            # don't return to the same place where we've already been unless we have fewer steps (more steps to make)
            key = (nr, nc, nhead)
            if key in tried and nsteps >= tried[key]:
                continue
            tried[key] = nsteps
            nloss = grid.get(nr, nc)
            heapq.heappush(q, (loss + nloss + end[0] - nr + end[1] - nc, loss + nloss, nr, nc, nhead, nsteps))
    assert False, "Path not found"


def part1(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    return min_heat_loss(grid, (0,0), (grid.h-1, grid.w-1))


e.run_tests(1, part1)
e.run_main(1, part1)


def can_turn(row, col, head, max_row, max_col):
    MIN_MOVE = 4
    if head == RIGHT:
        return max_col - 1 - col >= MIN_MOVE
    if head == LEFT:
        return col >= MIN_MOVE
    if head == DOWN:
        return max_row - 1 - row >= MIN_MOVE
    if head == UP:
        return row >= MIN_MOVE
    assert False, f"Incorrect heading {head}"


def ultracrucible(grid, start, end):
    # (heuristic_key, loss_so_far, row, column, heading, steps_in_current_dir)
    q = [(0, 0, start[0], start[1], RIGHT, 0), (0, 0, start[0], start[1], DOWN, 0)]
    tried = defaultdict(set)
    while q:
        _, loss, row, col, head, steps = heapq.heappop(q)
        if (row, col) == end and steps >= 4:
            return loss
        follow = []
        if steps < 10:
            # forward
            follow.append((one_step_in_direction(row, col, head), steps + 1))
        if steps >= 4:
            # can turn
            # but only if we can make 4 steps in the new direction and stay within the grid
            left = (head - 1) % 4
            right = (head + 1) % 4
            if can_turn(row, col, left, grid.h, grid.w):
                follow.append((one_step_in_direction(row, col, left), 1))
            if can_turn(row, col, right, grid.h, grid.w):
                follow.append((one_step_in_direction(row, col, right), 1))
        for pos, nsteps in follow:
            nr, nc, nhead = pos
            if not grid.is_in(nr, nc):
                continue
            # don't return to the same place where we've already been unless we have different
            # number of steps (fewer or more, both can make a difference)
            key = (nr, nc, nhead)
            if key in tried and nsteps in tried[key]:
                continue
            tried[key].add(nsteps)
            nloss = grid.get(nr, nc)
            heapq.heappush(q, (loss + nloss + end[0] - nr + end[1] - nc, loss + nloss, nr, nc, nhead, nsteps))
    assert False, "Path not found"


def part2(input):
    grid = Grid(input.get_valid_lines(), ints=True)
    return ultracrucible(grid, (0,0), (grid.h-1, grid.w-1))


e.run_tests(2, part2)
e.run_main(2, part2)

