#!/usr/bin/python3.8

from pyaoc import Env

e = Env(19)
e.T("""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""", 79, 3621)

RANGE = 1000
OVERLAP_LIMIT = 12


def parse_readings(input):
    readings = []
    for g in input.get_groups():
        assert len(g) >= 2
        assert g[0].startswith('--- scanner')
        readings += [[]]
        for ln in g[1:]:
            c = [int(x) for x in ln.split(',')]
            assert len(c) == 3
            readings[-1] += [c]
    return readings


def transform(point, orient):
    # orient // 8 -> facing 0=x, 1=y, 2=z
    facing = orient // 8
    case = orient % 8
    # case // 4 -> facing positive, negative
    facing_dir = -1 if case // 4 else 1
    case2 = case % 4
    # up -> 0=x+1, 1=x+2
    up = (facing + 1 + case2 // 2) % 3
    up_dir = -1 if case2 % 2 else 1
    # side -> 0=x+2, 1=x+1
    side = (facing + 2 - (case2 // 2)) % 3
    case3 = facing_dir * up_dir
    side_dir = case3 if case2 // 2 == 0 else -case3

    return (facing_dir * point[facing], up_dir * point[up], side_dir * point[side])
    # print(f"{'-' if facing_dir < 0 else '+'}{chr(ord('x')+facing)}, {'-' if up_dir < 0 else '+'}{chr(ord('x')+up)}, {'-' if side_dir < 0 else '+'}{chr(ord('x')+side)}")


def match_points(A_set, B_points, A_pos, B_pos, orient):
    matching = 0
    for point_o in B_points:
        point_p = transform(point_o, orient)
        point = (point_p[0] + B_pos[0], point_p[1] + B_pos[1], point_p[2] + B_pos[2])
        if point in A_set:
            matching += 1
        else:
            # Here we could check whether the transformed 'point' is within the range of scanner A
            # and return False if it is. However, we don't know the coordinates of scanner A at this
            # point, so're just going to ignore this
            if max(abs(A_pos[i] - point[i]) for i in range(3)) <= RANGE:
                # The transformed point was supposed to have been visible to scanner A,
                # but we didn't find it in scanner A's reading, so this matching is
                # definitely wrong
                return False
    return matching >= OVERLAP_LIMIT


def find_overlap(scA, scB, scannerA_pos):
    scA_set = set()
    for r in scA:
        scA_set.add((r[0], r[1], r[2]))
    for orient in range(24):
        # for each of the possible orientations of scanner B w.r.t. scanner A
        for pointB_o in scB:
            # for each point of scanner B
            pointB = transform(pointB_o, orient)
            for pointA in scA:
                # assume that pointA from scanner A is the same as pointB from scanner B

                # calculate position of scanner B in scanner A coordinates
                scannerB_pos = (pointA[0] - pointB[0], pointA[1] - pointB[1], pointA[2] - pointB[2])

                # Try match the rest of scanner B points to scanner A points.
                # If there are any that should have been recorder by scanner A but weren't
                # then it's not a match. Otherwise, if there are at least 12 matching points,
                # then scanners A and B are overlapping, and we know the right orientation of
                # B w.r.t. A.
                if match_points(scA_set, scB, scannerA_pos, scannerB_pos, orient):
                    return scannerB_pos, orient
    return None, None


def transform_readings(reading, scanner_pos, orient):
    res = []
    for point in reading:
        t = transform(point, orient)
        res.append((t[0] + scanner_pos[0], t[1] + scanner_pos[1], t[2] + scanner_pos[2]))
    return res


def align_all_readings(readings):
    # scanner 0 is the one that defines the coordinate system and all others need to align to it
    aligned = set([0])
    transformed_scanners = {
        0: {'reading': readings[0], 'pos': (0,0,0)}
    }
    try_next = set([0])
    to_align = set([x for x in range(1, len(readings))])
    while to_align:
        if not try_next:
            assert False, "no new overlaps to try, this would be an infinite loop!"
        newly_aligned = set()
        for i in to_align:
            for j in try_next:
                aligned_reading = transformed_scanners[j]
                pos, orient = find_overlap(aligned_reading['reading'], readings[i], aligned_reading['pos'])
                if pos is not None:
                    #print(f"Overlap {i} with {j}. Pos {pos}, orient {orient}")
                    #print(f"Overlap {i} with {j}.")
                    # scanner i overlaps with scanner j
                    aligned.add(i)

                    # transform all points of scanner i to the coordinate system of scanner 0
                    transformed_scanners[i] = {
                        'reading': transform_readings(readings[i], pos, orient),
                        'pos': pos,
                    }

                    # now that scanner i is aligned, in the next iteration, try to match other
                    # scanners to i
                    newly_aligned.add(i)

                    # no need to try to align with any other already aligned scanners
                    break

        to_align = to_align - newly_aligned
        try_next = newly_aligned
        #if to_align:
        #    print(f"Left to align: {to_align}")
        print(f"Newly aligned: {newly_aligned}")
    return transformed_scanners


def part1(input):
    readings = parse_readings(input)
    assert len(readings) > 1

    transformed_scanners = align_all_readings(readings)

    # collect all unique points
    unique = set()
    for scanner in transformed_scanners.values():
        for pt in scanner['reading']:
            unique.add((pt[0], pt[1], pt[2]))

    return len(unique)


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    readings = parse_readings(input)
    assert len(readings) > 1

    transformed_scanners = align_all_readings(readings)

    # find max distance between scanners
    max_dist = 0
    for scA in transformed_scanners.values():
        for scB in transformed_scanners.values():
            p1 = scA['pos']
            p2 = scB['pos']
            d = sum(abs(p1[i]-p2[i]) for i in range(3))
            max_dist = max(max_dist, d)
    return max_dist


e.run_tests(2, part2)
e.run_main(2, part2)
