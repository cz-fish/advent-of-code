#!/usr/bin/python3.8

from aoc import Env
import re

e = Env(15, param={'y': 2000000, 'limit': 4000000})
e.T("""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""", 26, 56000011, {'y': 10, 'limit': 20})


number = re.compile(r'-?\d+')


def dist(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.sx = sx
        self.sy = sy
        self.bx = bx
        self.by = by
        self.strength = dist(sx, sy, bx, by)

    def interval(self, line):
        y_dist = abs(self.sy - line)
        if y_dist > self.strength:
            # no overlap, empty interval
            return [0, -1]
        # half of the horizontal size of the interval
        size = self.strength - y_dist
        # line overlap is the interval from i_min to i_max
        i_min = self.sx - size
        i_max = self.sx + size
        # Note: not excluding the beacon from the interval;
        # we'll have to remove all overlapping beacons later
        """
        # if the beacon is in the interval (it can only be on
        # one of the ends), shorten the interval to exclude the beacon
        if self.bx == i_min:
            i_min += 1
        if self.by == i_max:
            i_max -= 1
        """
        # if the ranges crossed, the interval will be considered empty
        return [i_min, i_max]


def parse_input(lines):
    sensors = []
    for ln in lines:
        numbers = [int(x) for x in number.findall(ln)]
        assert len(numbers) == 4
        sensors.append(Sensor(*numbers))
    return sensors


def merge_intervals(all):
    all.sort()
    merged = []
    for i in all:
        if i[1] < i[0]:
            # empty
            continue
        if merged and i[0] <= merged[-1][1] + 1:
            # merge overlapping
            merged[-1][1] = max(merged[-1][1], i[1])
        else:
            # append new non-overlapping
            merged.append(i)
    return merged


def count_included_beacons(intervals, beacons, line):
    count = 0
    for beacon in beacons:
        if beacon[1] != line:
            continue
        for i in intervals:
            if i[0] > beacon[0]:
                break
            if i[1] >= beacon[0]:
                count += 1
                break
    return count


def count_overlap(sensors, beacons, line):
    # for each sensor, find its overlap with the given line
    intervals = [s.interval(line) for s in sensors]
    # remove empty intervals and merge the rest
    intervals = merge_intervals(intervals)
    # sum sizes of the remaining intervals
    line_coverage = sum([i[1] - i[0] + 1 for i in intervals])
    beacons_included = count_included_beacons(intervals, beacons, line)
    print(f"line coverage {line_coverage}, beacons included {beacons_included}")
    return line_coverage - beacons_included


def part1(input):
    sensors = parse_input(input.get_valid_lines())
    beacons = set([(s.bx, s.by) for s in sensors])
    line = e.get_param()['y']
    return count_overlap(sensors, beacons, line)


e.run_tests(1, part1)
e.run_main(1, part1)


def clamp_intervals(intervals, limit):
    clamped = []
    for i in intervals:
        if i[1] < 0:
            continue
        if i[0] > limit:
            continue
        if i[0] < 0:
            clamped.append([0, min(i[1], limit)])
        elif i[1] > limit:
            clamped.append([i[0], limit])
        else:
            clamped.append(i)
    return clamped


def find_empty(sensors, limit):
    for line in range(0, limit+1):
        #if line % 10000 == 0:
        #    print("line", line)
        # for each sensor, find its overlap with the given line
        intervals = [s.interval(line) for s in sensors]
        intervals = clamp_intervals(merge_intervals(intervals), limit)
        if len(intervals) > 1:
            assert len(intervals) == 2
            bx = intervals[0][1] + 1
            assert bx == intervals[1][0] - 1
            return bx, line
        elif not intervals:
            assert False, "whole empty line"
        elif intervals[0][0] > 0:
            assert intervals[0][0] == 1
            return 0, line
        elif intervals[0][1] < limit:
            assert intervals[0][1] == limit - 1
            return limit, line
    assert False, "no empty position found"


def part2(input):
    sensors = parse_input(input.get_valid_lines())
    beacons = set([(s.bx, s.by) for s in sensors])
    limit = e.get_param()['limit']
    x, y = find_empty(sensors, limit)
    print(f"empty position {x}, {y}")
    return x * 4000000 + y


e.run_tests(2, part2)
e.run_main(2, part2)
