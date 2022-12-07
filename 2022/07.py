#!/usr/bin/python3.8

from aoc import Env
from dataclasses import dataclass
from typing import Dict

e = Env(7)
e.T("""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""", 95437, 24933642)


@dataclass
class Node:
    name: str
    size: int
    is_dir: bool
    parent: None
    contents: dict


def make_tree(lines):
    root = Node(name='/', size=0, is_dir=True, parent=None, contents={})
    node = root
    for ln in lines:
        if ln.startswith('$ '):
            # command
            cmd = ln[2:4]
            if cmd == 'cd':
                where = ln[5:]
                if where == '/':
                    node = root
                elif where == '..':
                    assert node.parent is not None, f"cd to parent from node {node}"
                    node = node.parent
                else:
                    assert where in node.contents, f"cd to subdir '{where}' that doesn't exist in node {node}"
                    node = node.contents[where]
            elif cmd == 'ls':
                # ignore
                pass
        elif ln.startswith('dir'):
            # subdir
            name = ln[4:]
            assert name not in node.contents, f"Duplicate name '{name}' in node {node}"
            node.contents[name] = Node(name=name, size=0, is_dir=True, parent=node, contents={})
        else:
            # file
            size_str, name = ln.split(' ')
            assert name not in node.contents, f"Duplicate name '{name}' in node {node}"
            node.contents[name] = Node(name=name, size=int(size_str), is_dir=False, parent=node, contents=None)
    return root


def print_tree(tree, level=0):
    indent = ' ' * level
    print(f'{indent}- {tree.name} ({"dir" if tree.is_dir else "file"}, size={tree.size})')
    if tree.is_dir:
        for sub in tree.contents.values():
            print_tree(sub, level+2)


def calc_dir_sizes(tree):
    if tree.is_dir:
        total = 0
        for sub in tree.contents.values():
            total += calc_dir_sizes(sub)
        tree.size = total
    return tree.size


def sum_small_dirs(tree, small_limit):
    total = 0
    if tree.is_dir:
        if tree.size <= small_limit:
            total += tree.size
        for sub in tree.contents.values():
            if sub.is_dir:
                total += sum_small_dirs(sub, small_limit)
    return total


def part1(input):
    tree = make_tree(input.get_valid_lines())
    calc_dir_sizes(tree)
    #print_tree(tree)
    return sum_small_dirs(tree, 100000)


e.run_tests(1, part1)
e.run_main(1, part1)


fs_size = 70000000
space_needed = 30000000


def find_smallest_bigger_than(tree, needed):
    if tree.is_dir:
        if tree.size < needed:
            return None
        best = tree.size
        for sub in tree.contents.values():
            if not sub.is_dir:
                continue
            candidate = find_smallest_bigger_than(sub, needed)
            if candidate is not None:
                best = min(best, candidate)
    return best


def part2(input):
    tree = make_tree(input.get_valid_lines())
    calc_dir_sizes(tree)
    used = tree.size
    free = fs_size - used
    needed = space_needed - free
    print(f"capacity {fs_size}, used {used}, free {free}, need to clean {needed}")
    return find_smallest_bigger_than(tree, needed)


e.run_tests(2, part2)
e.run_main(2, part2)
