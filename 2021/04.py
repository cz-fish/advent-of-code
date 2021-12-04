#!/usr/bin/python3.8

from aoc import Env
from collections import defaultdict
import re

e = Env(4)
e.T("""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""", 4512, 1924)


class Bingo():
    def __init__(self, lines):
        self.nums = [int(x) for x in lines[0].split(',')]
        assert(len(lines) % 5 == 1)
        self.tickets = []
        self.numsOnTicket = defaultdict(list)
        counter = 0
        for i in range(1, len(lines), 5):
            self.tickets += [self._parseTicket(counter, lines[i:i+5])]
            counter += 1

    def _parseTicket(self, number, lines):
        r = re.compile(r'\d+')
        nums = [[int(x) for x in r.findall(ln)] for ln in lines]
        ticket = {
            'rows': [],
            'cols': []
        }
        for row in nums:
            ticket['rows'] += [set()]
            for num in row:
                ticket['rows'][-1].add(num)
                self.numsOnTicket[num] += [number]
        for i in range(len(nums[0])):
            ticket['cols'] += [set()]
            for j in range(len(nums)):
                ticket['cols'][-1].add(nums[j][i])
        return ticket

    def __str__(self):
        v = f"Bingo nums {self.nums}, tickets {len(self.tickets)}\n"
        for i, t in enumerate(self.tickets):
            v += f"[{i}] {t['rows']} {t['cols']}\n"
        return v

    def play1(self):
        for num in self.nums:
            for ticketNr in self.numsOnTicket[num]:
                bingo = self.crossNumberOnTicket(num, ticketNr)
                if bingo:
                    return num * self.sumTicket(ticketNr)
        assert(False, "No ticket won")

    def crossNumberOnTicket(self, num, ticketNr):
        ticket = self.tickets[ticketNr]
        bingo = False
        for row in ticket['rows']:
            if num in row:
                row.remove(num)
                if len(row) == 0:
                    bingo = True
                break
        for col in ticket['cols']:
            if num in col:
                col.remove(num)
                if len(col) == 0:
                    bingo = True
                break
        return bingo
    
    def sumTicket(self, ticketNr):
        ticket = self.tickets[ticketNr]
        s = 0
        for row in ticket['rows']:
            s += sum(list(row))
        return s

    def play2(self):
        winning = set()
        for num in self.nums:
            for ticketNr in self.numsOnTicket[num]:
                if ticketNr not in winning:
                    bingo = self.crossNumberOnTicket(num, ticketNr)
                    if bingo:
                        winning.add(ticketNr)
                        if len(winning) == len(self.tickets):
                            return num * self.sumTicket(ticketNr)
        assert(False, "Some tickets didn't win")



def part1(input):
    bingo = Bingo(input.get_valid_lines())
    # print(bingo)
    return bingo.play1()


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    bingo = Bingo(input.get_valid_lines())
    return bingo.play2()


e.run_tests(2, part2)
e.run_main(2, part2)
