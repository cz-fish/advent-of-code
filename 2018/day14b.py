#!/usr/bin/env python3

def solve(n):
    vl = len(n)
    ll = [3, 7]
    p1 = 0
    p2 = 1
    xs = '37'
    cnt = 0
    while True:
        cnt += 1
        v1 = ll[p1]
        v2 = ll[p2]
        s = v1 + v2
        if s >= 10:
            ll += [s // 10]
            xs += str(ll[-1])
        ll += [s % 10]
        xs += str(ll[-1])
        p1 = (p1 + 1 + v1) % len(ll)
        p2 = (p2 + 1 + v2) % len(ll)
        xl = len(xs)
        if xl >= vl + 1:
            if xs[-vl-1:-1] == n:
                return xl - vl - 1
        if xl >= vl:
            if xs[-vl:] == n:
                return xl - vl

print(solve('51589'))
print(solve('01245'))
print(solve('92510'))
print(solve('59414'))
print(solve('440231'))
