#!/usr/bin/env python3

nums = []

with open('day8.txt', 'rt') as f:
    l = f.readline()
    nums = [int(i) for i in l.strip().split(' ')]

class Node:
    def __init__(self):
        pass
        
    def make(self, nums, pos):
        self.n_child = nums[pos]
        self.n_meta = nums[pos+1]
        self.child = []
        pos += 2
        for i in range(self.n_child):
            n = Node()
            pos = n.make(nums, pos)
            self.child += [n]
        self.meta = nums[pos:pos + self.n_meta]
        return pos + self.n_meta

    def sum(self):
        s = 0
        for c in self.child:
            s += c.sum()
        s += sum(self.meta)
        return s

    def value(self):
        if self.n_child == 0:
            return sum(self.meta)
        s = 0
        for m in self.meta:
            if m == 0 or m > self.n_child: continue
            s += self.child[m-1].value()
        return s

tree = Node()
tree.make(nums, 0)
print(tree.sum())
print(tree.value())