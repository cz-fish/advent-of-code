#!/usr/bin/python3.8

import re

class Passport:
    def __init__(self):
        self.fields = {}
    
    def add(self, fields):
        for k, v in fields:
            self.fields[k] = v
    
    def valid_fields(self):
        return (len(self.fields) == 8) or (len(self.fields) == 7 and 'cid' not in self.fields)
    
    def in_range(self, field, mm, MM):
        v = int(self.fields[field])
        return v >= mm and v <= MM

    def valid_height(self):
        m = re.match(r'^(\d+)(in|cm)$', self.fields['hgt'])
        if m is None:
            return False
        h = int(m.group(1))
        u = m.group(2)
        return (u == 'in' and h >= 59 and h <= 76) or (u == 'cm' and h >= 150 and h <= 193)

    def valid_hair(self):
        return re.match(r'^#[0-9a-f]{6}$', self.fields['hcl']) is not None

    def valid_eye(self):
        return self.fields['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def valid_pid(self):
        return re.match(r'^\d{9}$', self.fields['pid']) is not None

    def valid_values(self):
        v = self.valid_fields() \
            and self.in_range('byr', 1920, 2002) \
            and self.in_range('iyr', 2010, 2020) \
            and self.in_range('eyr', 2020, 2030) \
            and self.valid_height() \
            and self.valid_hair() \
            and self.valid_eye() \
            and self.valid_pid()
        return v


passports = [Passport()]
with open('input04.txt', 'rt') as f:
    for ln in f.readlines():
        ln = ln.strip()
        if not ln:
            passports += [Passport()]
            continue
        parts = [tuple(b.split(':')) for b in ln.split(' ')]
        passports[-1].add(parts)

# Part 1
valid = len([1 for p in passports if p.valid_fields()])
print(f"Part1: Valid passports: {valid}")

# Part 2
valid = len([1 for p in passports if p.valid_values()])
print(f"Part2: Valid passports: {valid}")
