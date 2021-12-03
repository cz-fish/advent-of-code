#!/usr/bin/env python3

import re

def weaknesses(special):
    prt = re.search(r'weak to ([^;]+)', special)
    if not prt: return []
    return prt.group(1).split(', ')

def immunities(special):
    prt = re.search(r'immune to ([^;]+)', special)
    if not prt: return []
    return prt.group(1).split(', ')

def damage(ata, defe):
    if ata.atype in defe.immune:
        return 0
    dmg = ata.effective
    if ata.atype in defe.weak:
        dmg *= 2
    return dmg

class Group:
    def __init__(self, id, iid, type, size, hp, special, ap, atype, initiative):
        self.id = id
        self.iid = iid
        self.type = type
        self.size = int(size)
        self.hp = int(hp)
        if special:
            special = special[1:-2]
            self.weak = weaknesses(special)
            self.immune = immunities(special)
        else:
            self.weak = []
            self.immune = []
        self.ap = int(ap)
        self.atype = atype
        self.initiative = int(initiative)
        self.effective = self.ap * self.size

    def __repr__(self):
        return """{{[{}] {} Group {}: {{ size: {}, hp: {}, ap: {} {}, ini: {}, effe: {}, weak: [{}], immune: [{}] }}}}""".format(
            self.id, self.type, self.iid, self.size, self.hp, self.ap, self.atype, self.initiative,
            self.effective, ', '.join(self.weak), ', '.join(self.immune))

    def select_target(self, immune, infect, chosen):
        if self.type == 'IS': tgt = infect
        else: tgt = immune

        most_dmg = None
        most_efe = None
        most_ini = None
        tgt_id = None
        for ene in tgt:
            if ene.id in chosen:
                continue
            dmg = damage(self, ene)
            if dmg == 0:
                continue
            #print("{} group {} would deal {} group {} {} damage".format(
            #    self.type, self.iid, ene.type, ene.iid, dmg))
            if most_dmg is None or dmg > most_dmg or \
                (dmg == most_dmg and ene.effective > most_efe) or \
                (dmg == most_dmg and ene.effective == most_efe and ene.initiative > most_ini):
                most_dmg = dmg
                most_efe = ene.effective
                most_ini = ene.initiative
                tgt_id = ene.id
        if most_dmg is None:
            return None
        return tgt_id
    
    def attacked_by(self, ot):
        dmg = ot.effective
        if ot.atype in self.immune:
            dmg = 0
        elif ot.atype in self.weak:
            dmg *= 2
        loss = dmg // self.hp
        #print("{} group {} attacks defending group {}, dmg {}, kills {} ({}) units".format(
        #    ot.type, ot.iid, self.iid, dmg, loss, min(loss, self.size)))
        self.size = max(0, self.size - loss)
        self.effective = self.ap * self.size

    def dead(self):
        return self.size <= 0


immune = []
infect = []
by_gid = {}

tgt = None
ty = None
counter = 0
iid = 0
with open('inputs/day24.txt', 'rt') as f:
    for ll in f.readlines():
        ll = ll.strip()
        if ll == 'Immune System:':
            tgt = immune
            ty = 'IS'
            iid = 1
        elif ll == 'Infection:':
            tgt = infect
            ty = 'F'
            iid = 1
        elif ll:
            m = re.match(r'^(\d+) units each with (\d+) hit points (\([^)]+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)', ll)
            if not m:
                print("no match", ll) 
                continue
            tgt += [Group(counter, iid, ty, *m.groups())]
            by_gid[counter] = tgt[-1]
            counter += 1
            iid += 1

def print_all():
    print("---------------------------")
    print("Immune system")
    for x in immune:
        print(x)

    print("Infection")
    for x in infect:
        print(x)
    print("---------------------------")

print_all()

round = 0
while immune and infect:
    round += 1
    if round % 100 == 0:
        print(round)
        print_all()

    all = immune + infect
    all.sort(key = lambda x: (x.effective, x.initiative), reverse=True)
    targets = {}
    for g in all:
        targets[g.id] = g.select_target(immune, infect, targets.values())

    dead = set()
    all.sort(key = lambda x: x.initiative, reverse=True)
    for g in all:
        if g.dead(): continue
        tid = targets[g.id]
        if tid is None: continue
        t = by_gid[tid]
        t.attacked_by(g)
    
    immune = [i for i in immune if not i.dead()]
    infect = [i for i in infect if not i.dead()]

    #print_all()

print_all()
print("------------")
print("Immunity left:", sum([x.size for x in immune]))
print("Infection left:", sum([x.size for x in infect]))
