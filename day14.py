#!/usr/bin/env python3

def solve(n):
    ll = [3, 7]
    p1 = 0
    p2 = 1
    while len(ll) < n + 10:
        v1 = ll[p1]
        v2 = ll[p2]
        s = v1 + v2
        if s >= 10:
            ll += [s // 10]
        ll += [s % 10]
        p1 = (p1 + 1 + v1) % len(ll)
        p2 = (p2 + 1 + v2) % len(ll)
    
    return ''.join([str(x) for x in ll[n:n+10]])

print(solve(9))
print(solve(5))
print(solve(18))
print(solve(2018))
print(solve(440231))
