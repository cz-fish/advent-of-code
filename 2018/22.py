#!/usr/bin/python3.8

from aoc import Env
from collections import deque
import heapq

e = Env(22)
e.T("""depth: 510
target: 10,10""", 114, 45)


MODULO = 20183


def parse_input(input):
    lines = input.get_valid_lines()
    assert lines[0].startswith('depth: ')
    assert lines[1].startswith('target: ')
    depth = int(lines[0][7:])
    target = [int(x) for x in lines[1][8:].split(',')]
    assert len(target) == 2
    return depth, target[0], target[1]


class Caves:
    def __init__(self, depth, tx, ty):
        self.depth = depth
        self.tx = tx
        self.ty = ty
        self.levels = {}

    def _find_region_type(self, x, y):
        p = (x, y)
        if p not in self.levels:
            q = deque()
            q.append(((x, y), None, None))
            while q:
                w, value_up, value_left = q.pop()
                if w in self.levels:
                    continue
                x, y = w
                if (x == 0 and y == 0) or (x == self.tx and y == self.ty):
                    self.levels[w] = (0 + self.depth) % MODULO
                    continue
                if value_left is None:
                    if x == 0:
                        value_up = y * 48271
                        value_left = 1
                    elif (x-1, y) in self.levels:
                        value_left = self.levels[(x-1, y)]
                if value_up is None:
                    if y == 0:
                        value_left = x * 16807
                        value_up = 1
                    elif (x, y-1) in self.levels:
                        value_up = self.levels[(x, y-1)]
                if value_left is not None and value_up is not None:
                    self.levels[w] = (value_left * value_up + self.depth) % MODULO
                else:
                    q.append((w, value_up, value_left))
                    if value_left is None:
                        q.append(((x-1, y), None, None))
                    if value_up is None:
                        q.append(((x, y-1), None, None))
        return self.levels[p]

    def print_region(self, left, top, right, bottom):
        for y in range(top, bottom + 1):
            line = ''
            for x in range(left, right + 1):
                if x == 0 and y == 0:
                    line += 'M'
                    continue
                if x == self.tx and y == self.ty:
                    line += 'T'
                    continue
                level = self._find_region_type(x, y)
                reg_type = '.=|'[level % 3]
                line += reg_type
            print(line)

    def sum_risk_level(self):
        self._find_region_type(self.tx, self.ty)
        total_risk = 0
        for y in range(0, self.ty + 1):
            for x in range(0, self.tx + 1):
                level = self._find_region_type(x, y)
                total_risk += level % 3
        return total_risk

    def find_friend(self):
        # precalculate regions at least in the given rectangle
        self._find_region_type(self.tx, self.ty)
        
        tools = 'NTC' # neither, torch, climbing
        TORCH = 1
        # Ordered tools in such a way that tool with index X is not allowed
        # in region with type X
        # 0 rocky: 1 torch, 2 climbing
        # 1 wet: 0 neither, 2 climbing
        # 2 narrow: 0 neither, 1 torch

        def dist(p):
            return abs(self.tx - p[0]) + abs(self.ty - p[1])
        def rtype(p):
            return self._find_region_type(p[0], p[1]) % 3
        def switch_tool(tool, region):
            tool = (tool + 1) % 3
            if tool == region:
                tool = (tool + 1) % 3
            return tool

        pos = (0, 0)
        time = 0
        tool = TORCH
        region = rtype(pos)
        switched = False
        min_dists = {}
        q = []
        heapq.heappush(q, (time + dist(pos), time, pos, tool, region, switched))
        count = 0
        while q:
            _, time, pos, tool, region, switched = heapq.heappop(q)
            
            count += 1
            #if count % 10000 == 0:
            #    print(f"step {count}: time={time}, pos={pos}, tool={tool}, region={region}, switched={switched}, queue={len(q)}")

            key = (pos[0], pos[1], tool)
            if key in min_dists and min_dists[key] <= time:
                # we've already managed to get here faster before
                continue
            min_dists[key] = time

            if pos[0] == self.tx and pos[1] == self.ty and tool == TORCH:
                # found him!
                print(f"found him after {count} cycles")
                return time
            # switching tool is one option
            if not switched:
                new_tool = switch_tool(tool, region)
                new_time = time + 7
                heapq.heappush(q, (new_time + dist(pos), new_time, pos, new_tool, region, True))
            # moving is another option
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx = pos[0] + dx
                ny = pos[1] + dy
                if nx < 0 or ny < 0:
                    # out of map
                    continue
                new_pos = (nx, ny)
                key = (nx, ny, tool)
                if key in min_dists and min_dists[key] <= time + 1:
                    # we already know a better path to the next position
                    continue
                new_region = rtype(new_pos)
                if new_region == tool:
                    # can't go with the current tool
                    continue
                new_time = time + 1
                heapq.heappush(q, (new_time + dist(new_pos), new_time, new_pos, tool, new_region, False))
            
        assert False, "All paths exhausted, didn't find the friend!"


def part1(input):
    depth, tx, ty = parse_input(input)
    caves = Caves(depth, tx, ty)
    if tx < 20 and ty < 20:
        caves.print_region(0, 0, tx + 5, ty + 5)
    return caves.sum_risk_level()


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    depth, tx, ty = parse_input(input)
    caves = Caves(depth, tx, ty)
    return caves.find_friend()


e.run_tests(2, part2)
e.run_main(2, part2)
