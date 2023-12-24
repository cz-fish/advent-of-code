#!/usr/bin/python3.8

from aoc import Env
import re
from dataclasses import dataclass
import numpy as np

e = Env(24, param=(200000000000000, 400000000000000))
e.T("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 2, 47, param=(7, 27))

@dataclass
class point:
    x: int
    y: int
    z: int

@dataclass
class hail:
    p: point
    d: point

@dataclass
class intsect:
    x: float
    y: float
    t_a: float
    t_b: float


def parse_input(input):
    hails = []
    r = re.compile(r'-?\d+')
    for ln in input.get_valid_lines():
        nums = [int(x) for x in r.findall(ln)]
        assert len(nums) == 6
        assert 0 not in nums
        hails.append(hail(p=point(x=nums[0], y=nums[1], z=nums[2]), d=point(x=nums[3], y=nums[4], z=nums[5])))
    return hails


def close(x0, y0, x1, y1):
    D = 1
    return abs(x0-x1) < D and abs(y0-y1) < D


def intersect_x_y(a: hail, b: hail):
    div = b.d.x * a.d.y - b.d.y * a.d.x
    if div == 0:
        return None
    v = a.d.x * (b.p.y - a.p.y) - a.d.y * (b.p.x - a.p.x)
    t_b = v / div
    if a.d.x == 0:
        return None
    t_a = (b.p.x - a.p.x + t_b * b.d.x) / a.d.x
    x = a.p.x + t_a * a.d.x
    check_x = b.p.x + t_b * b.d.x
    y = a.p.y + t_a * a.d.y
    check_y = b.p.y + t_b * b.d.y
    #assert close(x, y, check_x, check_y), f"{x} {check_x}, {y} {check_y}"
    return intsect(x=x, y=y, t_a=t_a, t_b=t_b)


def in_bounds(intersection, lower, upper):
    if intersection is None:
        return False
    if intersection.t_a <= 0 or intersection.t_b <= 0:
        return False
    return intersection.x >= lower and intersection.x <= upper and intersection.y >= lower and intersection.y <= upper


def part1(input):
    hails = parse_input(input)
    lower, upper = e.get_param()
    total = 0
    for i, first in enumerate(hails):
        for second in hails[i+1:]:
            if in_bounds(intersect_x_y(first, second), lower, upper):
                total += 1
    return total


e.run_tests(1, part1)
e.run_main(1, part1)


def ranges(points):
    mx = points[0].x
    Mx = points[0].x
    my = points[0].y
    My = points[0].y
    mz = points[0].z
    Mz = points[0].z
    for i in range(1, len(points)):
        mx = min(mx, points[i].x)
        Mx = max(Mx, points[i].x)
        my = min(my, points[i].y)
        My = max(My, points[i].y)
        mz = min(mz, points[i].z)
        Mz = max(Mz, points[i].z)
    return mx, Mx, my, My, mz, Mz


def move_steps(hails, step):
    points = []
    for hail in hails:
        points.append(point(
            x=hail.p.x + step * hail.d.x,
            y=hail.p.y + step * hail.d.y,
            z=hail.p.z + step * hail.d.z
        ))
    return points


def solve_linear_eq(hails, velocity):
    rights = [0] * (len(hails) * 3)
    lefts = [
        [0 for _ in range(len(hails) + 3)]
        for _ in range(len(hails) * 3)
    ]
    x_idx = len(hails) + 0
    y_idx = len(hails) + 1
    z_idx = len(hails) + 2
    for i, hail in enumerate(hails):
        eq_idx = i * 3
        rights[eq_idx + 0] = -hail.p.x
        rights[eq_idx + 1] = -hail.p.y
        rights[eq_idx + 2] = -hail.p.z
        lefts[eq_idx + 0][i] = hail.d.x - velocity.x
        lefts[eq_idx + 1][i] = hail.d.y - velocity.y
        lefts[eq_idx + 2][i] = hail.d.z - velocity.z
        lefts[eq_idx + 0][x_idx] = -1
        lefts[eq_idx + 1][y_idx] = -1
        lefts[eq_idx + 2][z_idx] = -1
    a = np.array(lefts[:len(hails)+3])
    b = np.array(rights[:len(hails)+3])
    if velocity.x == -3 and velocity.y == 1 and velocity.z == 2:
        for i in range(len(lefts)):
            ln = ""
            w = len(hails)
            for j in range(w):
                t = lefts[i][j]
                ln += f" {'+' if t >= 0 else ''}{t} t{j}"
            ln += f" {'+' if lefts[i][w] >= 0 else ''}{lefts[i][w]} x"
            ln += f" {'+' if lefts[i][w+1] >= 0 else ''}{lefts[i][w+1]} y"
            ln += f" {'+' if lefts[i][w+2] >= 0 else ''}{lefts[i][w+2]} z"
            ln += f" = {rights[i]}"
            print(ln)
        #print(lefts)
        #print(rights)
    try:
        x = np.linalg.solve(a, b)
        return point(x=x[x_idx], y=x[y_idx], z=x[z_idx])
    except np.linalg.LinAlgError as e:
        #print(e)
        return None


def is_viable(dv, v, all_vs, all_dvs):
    for i in range(len(all_vs)):
        x = all_vs[i]
        dx = all_dvs[i]
        top = v - x
        bottom = dx - dv
        if bottom == 0:
            if top != 0:
                return False
            continue
        if top % bottom != 0:
            return False
        div = top // bottom
        if div < 0:
            return False
    return True


def find_viable_x_y_z(hails):
    xs = [h.p.x for h in hails]
    ys = [h.p.y for h in hails]
    zs = [h.p.z for h in hails]
    dxs = [h.d.x for h in hails]
    dys = [h.d.y for h in hails]
    dzs = [h.d.z for h in hails]
    viable_x = set()
    viable_y = set()
    viable_z = set()
    wrong_x = set()
    wrong_y = set()
    wrong_z = set()
    for i, dx in enumerate(dxs):
        if is_viable(dx, xs[i], xs, dxs):
            viable_x.add((dx, xs[i]))
        else:
            wrong_x.add(dx)
    for i, dy in enumerate(dys):
        if is_viable(dy, ys[i], ys, dys):
            viable_y.add((dy, ys[i]))
        else:
            wrong_y.add(dy)
    for i, dz in enumerate(dzs):
        if is_viable(dz, zs[i], zs, dzs):
            viable_z.add((dz, zs[i]))
        else:
            wrong_z.add(dz)
    print(f"viable dX-s: {viable_x}")
    print(f"viable dY-s: {viable_y}")
    print(f"viable dZ-s: {viable_z}")


def inspect(hails):
    coords = {}

    def check(i, p, d, c):
        nonlocal coords
        key = (p, d, c)
        if key in coords:
            print(f"{i} and {coords[key]}")
            print(hail)
            print(hails[coords[key]])
        else:
            coords[key] = i

    for i, hail in enumerate(hails):
        check(i, hail.p.x, hail.d.x, 'x')
        check(i, hail.p.y, hail.d.y, 'y')
        check(i, hail.p.z, hail.d.z, 'z')
    print(len(coords))


def intersection(first, second, dx, dy):
    a = hail(p=first.p, d=point(x=first.d.x + dx, y=first.d.y + dy, z=0))
    b = hail(p=second.p, d=point(x=second.d.x + dx, y=second.d.y + dy, z=0))
    i = intersect_x_y(a, b)
    if i is None:
        return None, None
    return i.t_b, (i.x, i.y)


def try_all_velocity(hails):
    assert len(hails) >= 4
    # Try all velocities Vx and Vy in range (-limit, limit) (starting from 0 and increasing)
    limit = 300
    for dx in range(2 * limit + 1):
        vx = (1 if (dx % 2) else -1) * (dx // 2)
        for dy in range(2 * limit + 1):
            vy = (1 if (dy % 2) else - 1) * (dy // 2)
            # Having Vx and Vy, take 4 hails. Adjust the velocities by Vx, Vy,
            # as if the rock wasn't moving and the hails were moving towards it.
            # If the Vx, Vy are the right velocities then the 4 lines should
            # intersect in the same point (possibly different times). Other
            # hails should intersect at that point as well, but we only check 4
            # and it's hopefully enough.
            t1, pos1 = intersection(hails[0], hails[1], vx, vy)
            if t1 is None:
                continue
            t2, pos2 = intersection(hails[0], hails[2], vx, vy)
            if t2 is None:
                continue
            t3, pos3 = intersection(hails[0], hails[3], vx, vy)
            if t3 is None:
                continue
            if pos1 != pos2 or pos1 != pos3:
                continue

            # If the Vx and Vy produce a match, check that Z coordinates match
            # as well
            for vz in range(-limit, limit+1):
                z1 = hails[1].p.z + t1 * (hails[1].d.z + vz)
                z2 = hails[2].p.z + t2 * (hails[2].d.z + vz)
                z3 = hails[3].p.z + t3 * (hails[3].d.z + vz)
                if z1 != z2 or z1 != z3:
                    continue
                print(f"t1 {t1} pos1 {pos1} z1 {z1}")
                print(f"t2 {t2} pos2 {pos2} z2 {z2}")
                print(f"t3 {t3} pos3 {pos3} z3 {z3}")
                print(f"vx {vx} vy {vy} vz {vz}")
                # Since the rock is not moving, the place when the hails
                # intersect must be the rock's position; so devise our
                # solution.
                return int(pos1[0]) + int(pos1[1]) + int(z1)
    print(f"Solution not found in range {-limit} .. {limit}")
    return None


def part2(input):
    hails = parse_input(input)

    if False:
        cr = ranges([p.p for p in hails])
        print(f"coord ranges: {cr[1]-cr[0]}, {cr[3]-cr[2]}, {cr[5]-cr[4]}")
        dr = ranges([p.d for p in hails])
        print(f"diff ranges: {dr}")
        #print(f"diff ranges: {dr[1]-dr[0]}, {dr[3]-dr[2]}, {dr[5]-dr[4]}")
        steps = [
            540000000000,
            541250000000,
            542500000000,
            545000000000,
            547500000000,
            548750000000,
            550000000000,
        ]
        for step in steps:
            points = move_steps(hails, step)
            #print(f"After {step} steps, coord range: {ranges(points)}")
            r = ranges(points)
            print(f"After {step} steps, coord ranges: {r[1]-r[0]}, {r[3]-r[2]}, {r[5]-r[4]}")

    if False:
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                for dz in range(-5, 6):
                    if dx == -3 and dy == 1 and dz == 2:
                        print("here")
                    s = solve_linear_eq(hails, point(x=dx, y=dy, z=dz))
                    if s is not None:
                        print(f"solution {s}")
                        return s.x + s.y + s.z
        print("solution not found")
    
    if False:
        find_viable_x_y_z(hails)
    
    if False:
        inspect(hails)

    if True:
        return try_all_velocity(hails)

    return 0


e.run_tests(2, part2)
e.run_main(2, part2)
