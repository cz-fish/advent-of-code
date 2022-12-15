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

def point_in_square(point, square):
    return point[0] >= square[0] and point[0] <= square[2] and point[1] >= square[1] and point[1] <= square[3]


class Sensor:
    def __init__(self, number, sx, sy, bx, by):
        self.number = number
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
    
    def covers(self, point):
        return self.strength >= dist(self.sx, self.sy, point[0], point[1])

    def __repr__(self):
        return f"[{self.number}: ({self.sx}, {self.sy}), {self.strength}]"


def parse_input(lines):
    sensors = []
    for i, ln in enumerate(lines):
        numbers = [int(x) for x in number.findall(ln)]
        assert len(numbers) == 4
        sensors.append(Sensor(i, *numbers))
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
    #print(f"line coverage {line_coverage}, beacons included {beacons_included}")
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


def part2_slower(input):
    sensors = parse_input(input.get_valid_lines())
    limit = e.get_param()['limit']
    x, y = find_empty(sensors, limit)
    print(f"empty position {x}, {y}")
    return x * 4000000 + y


def find_empty_subdividing(sensors, square):
    left, top, right, bottom = square
    width = right - left
    if width == 0:
        # single square
        if not sensors:
            return left, top
        return None, None
    else:
        # subdivide
        half = width // 2
        for subsquare in [
            (left, top, left + half, top + half),             # top left
            (left + half + 1, top, right, top + half),        # top right
            (left, top + half + 1, left + half, bottom),      # bottom left
            (left + half + 1, top + half + 1, right, bottom)  # bottom right
        ]:
            sleft, stop, sright, sbottom = subsquare
            subsensors = []
            fully_covered = False
            for sensor in sensors:
                corners_covered_by_sensor = sum([
                    1 for corner in [(sleft, stop), (sright, stop), (sleft, sbottom), (sright, sbottom)]
                    if sensor.covers(corner)])
                if corners_covered_by_sensor == 4:
                    fully_covered = True
                    break
                
                points_inside = sum([
                    1 for point in [
                        (sensor.sx, sensor.sy),
                        (sensor.sx, sensor.sy - sensor.strength),
                        (sensor.sx + sensor.strength, sensor.sy),
                        (sensor.sx, sensor.sy + sensor.strength),
                        (sensor.sx - sensor.strength, sensor.sy)
                    ] if point_in_square(point, subsquare)])

                if corners_covered_by_sensor > 0 or points_inside > 0:
                    subsensors.append(sensor)

            if fully_covered:
                # A single sensor covers the whole subsquare. There is definitely no empty position
                # in that subsquare
                continue

            x, y = find_empty_subdividing(subsensors, subsquare)
            if x is not None:
                return x, y
    return None, None


def part2(input):
    sensors = parse_input(input.get_valid_lines())
    limit = e.get_param()['limit']
    x, y = find_empty_subdividing(sensors, (0, 0, limit, limit))
    print(f"empty position {x}, {y}")
    # Check the result
    for sensor in sensors:
        if sensor.covers((x, y)):
            assert False, f"wrong result: sensor {sensor.number} ({sensor}) covers {x} {y}"
    return x * 4000000 + y


e.run_tests(2, part2)
e.run_main(2, part2)
