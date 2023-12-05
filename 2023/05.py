#!/usr/bin/python3.8

from aoc import Env

e = Env(5)
e.T("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""", 35, 46)

e.T("""seeds: 10 10

seed-to-location map:
20 9 5
""", None, 14)

e.T("""seeds: 10 10

seed-to-location map:
1 16 7
""", None, 1)

e.T("""seeds: 10 10

seed-to-location map:
22 10 10
""", None, 22)

e.T("""seeds: 10 10

seed-to-location map:
3 12 5
""", None, 3)

e.T("""seeds: 10 10

seed-to-location map:
20 10 6
3 16 4
""", None, 3)


def parse_maps(input):
    seeds = []
    map_maps = {}
    key = None
    for ln in input.get_valid_lines():
        if ln.startswith('seeds:'):
            seeds = [int(x) for x in ln[7:].split()]
        elif not ln:
            continue
        elif 'map:' in ln:
            source_to_dest, _ = ln.split()
            source, _, dest = source_to_dest.split('-')
            key = (source, dest)
            assert key not in map_maps
            map_maps[key] = []
        else:
            assert key is not None
            nums = [int(x) for x in ln.split()]
            assert len(nums) == 3
            map_maps[key].append(tuple(nums))
    return seeds, map_maps


def convert_value(val, map_map):
    for dest, source, count in map_map:
        end = source + count - 1
        if val >= source and val <= end:
            return dest + val - source
    return val


def seed_to_location(seed, map_maps):
    key = 'seed'
    val = seed
    #print(f"seed {val}")
    while key != 'location':
        for k, map_map in map_maps.items():
            if k[0] == key:
                key = k[1]
                val = convert_value(val, map_map)
                #print(f"{key} {val}")
                break
        else:
            assert False, f"cannot convert from {key}"
    #print("---")
    return val


def part1(input):
    seeds, map_maps = parse_maps(input)
    #print(f"seeds:\n{seeds}")
    #print(f"\nmap_maps:\n{map_maps}")
    locations = [seed_to_location(seed, map_maps) for seed in seeds]
    return min(locations)


e.run_tests(1, part1)
e.run_main(1, part1)


def convert_intervals(intervals, map_map):
    result = []
    while intervals:
        int_start, int_size = intervals.pop()
        int_end = int_start + int_size - 1
        for map_dest, map_start, map_size in map_map:
            map_end = map_start + map_size - 1
            if map_end < int_start or map_start > int_end:
                # interval and map don't overlap
                continue
            if map_start <= int_start and map_end >= int_end:
                # whole interval mapped
                off = int_start - map_start
                result.append((map_dest + off, int_size))
            elif map_start < int_start:
                # interval split in 2
                # left part of interval mapped
                off = int_start - map_start
                converted_size = map_size - off
                result.append((map_dest + off, converted_size))
                intervals.append((int_start + converted_size, int_size - converted_size))
            elif map_end > int_end:
                # interval split in 2
                # right part of interval mapped
                off = map_start - int_start
                intervals.append((int_start, off))
                result.append((map_dest, int_size - off))
            else:
                # interval split in 3
                # middle part of interval mapped
                left = map_start - int_start
                right = int_end - map_end
                intervals.append((int_start, left))
                intervals.append((map_end + 1, right))
                result.append((map_dest, int_size - left - right))
            break
        else:
            # interval not converted
            result.append((int_start, int_size))
    return result

def seed_interval_to_location(start, count, map_maps):
    key = 'seed'
    intervals = [(start, count)]
    while key != 'location':
        for k, map_map in map_maps.items():
            if k[0] == key:
                key = k[1]
                intervals = convert_intervals(intervals, map_map)
                break
        else:
            assert False, f"cannot convert from {key}"
    return intervals


def part2(input):
    seeds, map_maps = parse_maps(input)
    locations = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        count = seeds[i+1]
        location_min = min([interval[0] for interval in seed_interval_to_location(start, count, map_maps)])
        locations.append(location_min)
    return min(locations)


e.run_tests(2, part2)
e.run_main(2, part2)

