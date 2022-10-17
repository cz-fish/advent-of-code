#!/usr/bin/python3.8

from aoc import Env
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

e = Env(20)
e.T("^WNE$", 3, 0)
e.T("^ENWWW(NEEE|SSE(EE|N))$", 10, 0)
e.T("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18, 0)
e.T("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23, 0)
e.T("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31, 0)

@dataclass
class Node:
    parent: Optional['Node']
    start: int
    end: int
    alter: List['Node']
    next: Optional['Node']

@dataclass
class ExplorationState:
    x: int
    y: int
    node: Node
    child_idx: int

class Map:
    def __init__(self, regex):
        # strip the markers
        regex = regex[1:-1]
        leg_list = self._parse_regex(regex)
        #print(regex)
        #self._print_regex_list(leg_list)
        self._build(regex, leg_list)

    def _record_room(self, x, y):
        self.min_x = min(x, self.min_x)
        self.max_x = max(x, self.max_x)
        self.min_y = min(y, self.min_y)
        self.max_y = max(y, self.max_y)
        self.rooms.add((x, y))

    def _parse_regex(self, regex):
        # indexes of interesting characters
        interest = [(i, c) for i, c in enumerate(regex) if c in '()|']
        if not interest:
            return Node(parent=None, start=0, end=len(regex), alter=[], next=None)
        node = Node(parent=None, start=0, end=0, alter=[], next=None)
        root = node
        parents = []
        for i, c in interest:
            node.end = i
            if c == '(':
                parents.append(node)
                node = Node(parent=parents[-1], start=i+1, end=0, alter=[], next=None)
                parents[-1].alter.append(node)
            elif c == '|':
                node = Node(parent=parents[-1], start=i+1, end=0, alter=[], next=None)
                parents[-1].alter.append(node)
            elif c == ')':
                node = Node(parent=None, start=i+1, end=0, alter=[], next=None)
                parents[-1].next = node
                parents.pop()
        node.end = len(regex)
        return root

    def _print_regex_list(self, leg_list, indent=0):
        print(f'{" " * indent}{leg_list.start}..{leg_list.end}')
        for a in leg_list.alter:
            self._print_regex_list(a, indent+2)
        if leg_list.next:
            self._print_regex_list(leg_list.next, indent)

    def _build(self, regex, leg_list):
        self.doors = set()
        self.rooms = set()
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self._record_room(0, 0)
        state_stack = [ExplorationState(x=0, y=0, node=leg_list, child_idx=-1)]
        while state_stack:
            state = state_stack[-1]
            x = state.x
            y = state.y
            node = state.node
            if state.child_idx < 0:
                rex_part = regex[node.start:node.end]
                x, y = self._follow_regex(x, y, rex_part)
                state.x = x
                state.y = y
                state.child_idx = 0
            if state.child_idx < len(node.alter):
                state_stack.append(ExplorationState(x=x, y=y, node=node.alter[state.child_idx], child_idx=-1))
                state.child_idx += 1
            else:
                state_stack.pop()
                if node.next:
                    state_stack.append(ExplorationState(x=x, y=y, node=node.next, child_idx=-1))
        self._fill_walls()

    def _follow_regex(self, x, y, regex):
        dirs = {
            'E': (1, 0),
            'W': (-1, 0),
            'N': (0, -1),
            'S': (0, 1)
        }
        for c in regex:
            assert c in dirs, f"invalid instruction {c}"
            dx, dy = dirs[c]
            self.doors.add((x + dx, y + dy))
            x += 2 * dx
            y += 2 * dy
            self._record_room(x, y)
        return x, y

    def _fill_walls(self):
        self.walls = set()
        for x, y in self.rooms:
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                px = x + dx
                py = y + dy
                if (px, py) not in self.doors:
                    self.walls.add((px, py))
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                self.walls.add((x + dx, y + dy))

    def print_maze(self):
        for y in range(self.min_y - 1, self.max_y + 2):
            line = ''
            for x in range(self.min_x - 1, self.max_x + 2):
                if (x, y) in self.walls:
                    line += '#'
                elif (x, y) in self.doors:
                    if y % 2 == 0:
                        line += '|'
                    else:
                        line += '-'
                elif x == 0 and y == 0:
                    line += 'X'
                else:
                    line += '.'
            print(line)

    def furthest(self):
        dists = {(0, 0): 0}
        q = deque()
        q.append((0, 0, 0))
        while q:
            x, y, dist = q.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                px = x + dx
                py = y + dy
                if (px, py) in self.doors:
                    nx = px + dx
                    ny = py + dy
                    p = (nx, ny)
                    if p not in dists or dists[p] > dist + 1:
                        dists[p] = dist + 1
                        q.append((nx, ny, dist + 1))
        return max(dists.values())
    
    def count_distant_over(self, limit):
        visited = set()
        q = deque()
        q.append((0, 0, 0))
        while q:
            x, y, dist = q.popleft()
            p = (x, y)
            if p in visited or dist >= limit:
                continue
            visited.add(p)
            for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                px = x + dx
                py = y + dy
                if (px, py) in self.doors:
                    nx = px + dx
                    ny = py + dy
                    p = (nx, ny)
                    if p not in visited:
                        q.append((nx, ny, dist + 1))
        print(f"Rooms: {len(self.rooms)}, distance {limit} or closer: {len(visited)}")
        return len(self.rooms) - len(visited)


def part1(input):
    regex = input.get_valid_lines()[0]
    building = Map(regex)
    building.print_maze()
    return building.furthest()


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    regex = input.get_valid_lines()[0]
    building = Map(regex)
    return building.count_distant_over(1000)


e.run_tests(2, part2)
e.run_main(2, part2)
