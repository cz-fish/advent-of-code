#!/usr/bin/python3.12

from pyaoc import Env

e = Env(9)
e.T("""7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""", 50, 24)


def parse_input(input):
    points = []
    for ln in input.get_valid_lines():
        p = [int(x) for x in ln.split(',')]
        assert len(p) == 2
        points.append((p[0], p[1]))
    return points


def part1(input):
    points = parse_input(input)
    biggest = 0
    for first_i in range(len(points)):
        first = points[first_i]
        for second_i in range(first_i + 1, len(points)):
            second = points[second_i]
            size = (abs(second[0] - first[0]) + 1) * (abs(second[1] - first[1]) + 1)
            biggest = max(biggest, size)
    return biggest


#e.run_tests(1, part1)
#e.run_main(1, part1)

def intersect_coords(a, b, c, d):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    x4, y4 = d
    hor1 = (y1 == y2)
    hor2 = (y3 == y4)
    if hor1:
        if hor2:
            # both lines horizontal
            return False
            if y1 != y3:
                return False
            if max(x1, x2) <= min(x3, x4) or min(x1, x2) >= max(x3, x4):
                return False
            return True
        else:
            # first horizontal second vertical
            X = x3
            Y = y1
            if X < min(x1, x2) or X > max(x1, x2):
                return False
            if X == x1 or X == x2:
                return min(y3, y4) < Y and max(y3, y4) > Y
            if Y < min(y3, y4) or Y > max(y3, y4):
                return False
            if Y == y3 or Y == y4:
                return min(x1, x2) < X and max(x1, x2) > X
            return True
    else:
        if hor2:
            # first vertical second horizontal
            X = x1
            Y = y3
            if X < min(x3, x4) or X > max(x3, x4):
                return False
            if X == x3 or X == x4:
                return min(y1, y2) < Y and max(y1, y2) > Y
            if Y < min(y1, y2) or Y > max(y1, y2):
                return False
            if Y == y1 or Y == y2:
                return min(x3, x4) < X and max(x3, x4) > X
            return True
        else:
            # both vertical
            return False
            if x1 != x3:
                return False
            if max(y1, y2) <= min(y3, y4) or min(y1, y2) >= max(y3, y4):
                return False
            return True


def intersect(points, a, b, c, d):
    return intersect_coords(points[a], points[b], points[c], points[d])


def ccw_triangle(A, B, C):
    left = A[0]*B[1] - A[1]*B[0] \
        + B[0]*C[1] - B[1]*C[0] \
        + C[0]*A[1] - C[1]*A[0]
    return left >= 0


def point_in_rect(point, mx, my, MX, MY):
    return point[0] > mx and point[0] < MX \
        and point[1] > my and point[1] < MY


def all_red_green0(points, first, second, trace):
    if trace:
        print(f"corners {first}, {second}")
    # polygon formed by points in counter-clockwise.
    # The rectangle between first and second has to be
    # on the left side of every line segment
    for i in range(len(points)):
        j = (i+1) % len(points)
        A = points[i]
        B = points[j]
        # is triangle A-B-first CCW?
        left1 = A[0]*B[1] - A[1]*B[0] \
            + B[0]*first[1] - B[1]*first[0] \
            + first[0]*A[1] - first[1]*A[0]
        if left1 < 0:
            if trace:
                print(f" fail on first: {i}, {A}, {B}, {first}")
            return False
        # is triangle A-B-second CCW?
        left2 = A[0]*B[1] - A[1]*B[0] \
            + B[0]*second[1] - B[1]*second[0] \
            + second[0]*A[1] - second[1]*A[0]
        if left2 < 0:
            if trace:
                print(f" fail on second: {i}, {A}, {B}, {second}")
            return False
    return True


def all_red_green(points, first_i, second_i, trace):
    first = points[first_i]
    second = points[second_i]
    # Rectangle A B C D
    mX = min(first[0], second[0])
    mY = min(first[1], second[1])
    MX = max(first[0], second[0])
    MY = max(first[1], second[1])
    A = (mX, mY)
    B = (MX, mY)
    C = (MX, MY)
    D = (mX, MY)
    if trace:
        print(f"X {mX}-{MX}, Y {mY}-{MY}")
        print(f"ABCD {A} {B} {C} {D}")
    # Edges of the rectangle must not intersect the polygon
    for i in range(len(points)):
        j = (i+1) % len(points)
        if intersect_coords(points[i], points[j], A, B) \
            or intersect_coords(points[i], points[j], B, C) \
            or intersect_coords(points[i], points[j], C, D) \
            or intersect_coords(points[i], points[j], D, A):
            return False
        if point_in_rect(points[i], mX, mY, MX, MY) \
            or point_in_rect(points[j], mX, mY, MX, MY):
            return False
    # and the rectangle must be inside the polygon
    #  - if the point 'second' is on the left side of
    #    the edge leading to point 'first'
    prev_i = (first_i - 1) % len(points)
    if trace:
        print(points[prev_i], first, second)
    return ccw_triangle(points[prev_i], first, second)


def part2(input):
    points = parse_input(input)
    # Assumption checks:
    #   too big to solve graphically
    #   polygon is counter-clockwise, non self-intersecting
    if False:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        print(f"Limits: x: {min(xs)} - {max(xs)}, y: {min(ys)} - {max(ys)}")
        area = 0
        for i in range(len(points)):
            j = (i+1) % len(points)
            area += points[i][0] * points[j][1] - points[j][0] * points[i][1]
        area /= 2
        print(f"Area {area}, CW or CCW: {'CW' if area < 0 else 'CCW'}")

        for i in range(len(points)):
            k = (i + 1) % len(points)
            for j in range(i+1, len(points)):
                l = (j + 1) % len(points)
                if intersect(points, i, k, j, l):
                    print(f"Intersection between {i}-{k} and {j}-{l}")
                    return 0
        print("No self intersection")

    biggest = 0
    for first_i in range(len(points)):
        first = points[first_i]
        for second_i in range(first_i + 1, len(points)):
            second = points[second_i]
            size = (abs(second[0] - first[0]) + 1) * (abs(second[1] - first[1]) + 1)
            #trace = size == 40
            #if trace:
            #    print(size)
            if size > biggest and all_red_green(points, first_i, second_i, False):
                biggest = max(biggest, size)
    return biggest


e.run_tests(2, part2)
e.run_main(2, part2)

# 487137255 too low
