#!/usr/bin/python3.8

from pyaoc import Env
import re
from collections import deque
import heapq

from dataclasses import dataclass

e = Env(16)
e.T("""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""", 1651, 1707)


@dataclass
class Actor:
    pos: str
    time_left: int
    stopped: bool
    path: list

@dataclass
class State:
    actors: list
    value: int
    valves_turned: list
    valves_unturned: list

    def __lt__(self, other):
        a = (len(self.valves_unturned), self.value, self.actors[0].time_left + self.actors[1].time_left)
        b = (len(other.valves_unturned), other.value, other.actors[0].time_left + other.actors[1].time_left)
        return a < b

p2best = 0

class Map:
    def __init__(self):
        self.rates = {}
        self.adj = {}

    def add(self, valve, rate, leads):
        assert valve not in self.rates, f"valve {valve} redefined. New rate {rate}, old rate {self.rates[valve]}"
        self.rates[valve] = rate
        self.adj[valve] = leads

    def shortest_dist(self, start):
        distances = {}
        q = deque()
        q.append((start, 0))
        while q:
            valve, dist = q.popleft()
            if valve in distances:
                continue
            distances[valve] = dist
            for n in self.adj[valve]:
                if n in distances:
                    continue
                q.append((n, dist + 1))
        return distances

    @classmethod
    def make(cls, lines):
        map = Map()
        r = re.compile(r'Valve (?P<valve>..) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<leads>.*)')
        for ln in lines:
            m = r.match(ln)
            assert m is not None, f"line not matched: '{ln}'"
            valve = m['valve']
            rate = int(m['rate'])
            leads = m['leads'].split(', ')
            map.add(valve, rate, leads)
        return map

    def __repr__(self):
        valves = list(sorted(self.rates.keys()))
        s = f"{len(valves)} valves, {sum([1 for v in valves if self.rates[v] > 0])} non-zero ones\n"
        s += '    ' + ' '.join(valves) + '\n'
        s += '    ' + ' '.join([f"{self.rates[v]:2}" for v in valves])
        for v in valves:
            s += f'\n{v}: {self.adj[v]}'
        return s


class SimplerMap:
    def __init__(self):
        self.rates = {}
        self.distances = {}

    def add(self, valve, rate, distances):
        self.rates[valve] = rate
        self.distances[valve] = distances

    @classmethod
    def simplify(cls, full_map):
        map = SimplerMap()
        keep_valves = ['AA'] + [v for v in full_map.rates.keys() if full_map.rates[v] > 0]
        keep_valves.sort()
        keep_set = set(keep_valves)
        for valve in keep_valves:
            all_distances = full_map.shortest_dist(valve)
            keep_distances = {v: d for v, d in all_distances.items() if v in keep_set}
            map.add(valve, full_map.rates[valve], keep_distances)
        return map

    def __repr__(self):
        valves = list(sorted(self.rates.keys()))
        s = ''
        s += '    ' + ' '.join([f"{self.rates[v]:2}" for v in valves]) + '\n'
        s += '    ' + ' '.join(valves)
        for v in valves:
            s += '\n' + v + '  '
            s += ' '.join([f"{self.distances[v][n]:2}" for n in valves])
        return s

    def find_best_value(self, start, time_left, turned_valves):
        if time_left <= 0:
            return 0, ''

        # value of turning the valve at the current position, costing 1 time
        turn_value = self.rates[start] * (time_left - 1)
        if turn_value > 0:
            time_left -= 1
        best_value = turn_value
        best_path = ''

        # try proceeding with turning the current valve
        turned_valves.add(start)
        for n in self.distances[start].keys():
            if n in turned_valves:
                continue
            path_value, path = self.find_best_value(n, time_left - self.distances[start][n], turned_valves)
            if turn_value + path_value > best_value:
                best_path = path
                best_value = turn_value + path_value
        turned_valves.remove(start)

        return best_value, start + ', ' + best_path

    def find_best_value_with_help(self, start, elephant, time_left, elephant_time, turned_valves, stop, elephant_stop, value_so_far, valves_remaining, value_estimate):
        global p2best
        # Problem: who has more time is the one who moves next. However, because both are at
        # different positions, the one who moves first might have a longer distance to their
        # destination than the other one would.

        if (time_left <= 0 and elephant_time <= 0) or (stop and elephant_stop):
            return 0, ''

        estimate = value_so_far + value_estimate * (max(time_left, elephant_time) - 1)
        if estimate <= p2best:
            return 0, ''

        best_value = 0
        best_path = ''
        best_elephant = ''

        if time_left > 0 and not stop:
            # try moving first
            pos = start
            time = time_left

            # value of turning the valve at the current position, costing 1 time
            turn_value = self.rates[pos] * (time - 1)
            if turn_value > 0:
                time -= 1
            best_value = max(best_value, turn_value)

            # try yielding to the elephant
            if len(turned_valves) > 1:
                path_value, path = self.find_best_value_with_help(
                    pos,
                    elephant,
                    time,
                    elephant_time,
                    turned_valves,
                    True,
                    elephant_stop,
                    value_so_far + turn_value,
                    valves_remaining - 1,
                    value_estimate - self.rates[pos]
                    )
                if turn_value + path_value > best_value:
                    best_path = path
                    best_value = turn_value + path_value

            # try proceeding with another valve
            dist = self.distances[pos]
            for n in dist.keys():
                if n in turned_valves or dist[n] > time:
                    continue
                turned_valves.add(n)
                path_value, path = self.find_best_value_with_help(
                    n,
                    elephant,
                    time - dist[n],
                    elephant_time,
                    turned_valves,
                    False,
                    elephant_stop,
                    value_so_far + turn_value,
                    valves_remaining - 1,
                    value_estimate - self.rates[pos]
                    )
                if turn_value + path_value > best_value:
                    best_path = path
                    best_value = turn_value + path_value
                turned_valves.remove(n)

        #if start == 'EE' and time_left == 16 and sorted(list(turned_valves)) == ['AA','DD','EE','HH']:
        #if start == 'EE' and time_left == 16 and elephant == 'JJ' and sorted(list(turned_valves)) == ['AA','DD','EE','HH','JJ']:
        #    import pdb; pdb.set_trace()

        if elephant_time > 0 and not elephant_stop and len(turned_valves) > 1:
            # try moving elephant first
            pos = elephant
            time = elephant_time

            # value of turning the valve at the current position, costing 1 time
            turn_value = self.rates[pos] * (time - 1)
            if turn_value > 0:
                time -= 1
            if turn_value > best_value:
                best_value = turn_value
                best_elephant = ' e'

            # try yielding
            path_value, path = self.find_best_value_with_help(
                start,
                pos,
                time_left,
                time,
                turned_valves,
                stop,
                True,
                value_so_far + turn_value,
                valves_remaining - 1,
                value_estimate - self.rates[pos]
                )
            if turn_value + path_value > best_value:
                best_path = path
                best_value = turn_value + path_value
                best_elephant = ' e'

            # try proceeding with turning the current valve
            dist = self.distances[pos]
            for n in dist.keys():
                if n in turned_valves or dist[n] > time:
                    continue
                turned_valves.add(n)
                path_value, path = self.find_best_value_with_help(
                    start,
                    n,
                    time_left,
                    time - dist[n],
                    turned_valves,
                    stop,
                    False,
                    value_so_far + turn_value,
                    valves_remaining - 1,
                    value_estimate - self.rates[pos]
                    )
                if turn_value + path_value > best_value:
                    best_path = path
                    best_value = turn_value + path_value
                    best_elephant = ' e'
                turned_valves.remove(n)

        if best_value > p2best:
            p2best = best_value

        current_pos = f"[{start}({time_left}) {elephant}({elephant_time}){best_elephant}], "
        #print(current_pos + best_path)
        return best_value, current_pos + best_path

    def find_some_solution(self, time_left):
        # Find some hopefully good solution, even if it doesn't have to be the best.
        # To be used for pruning other states
        valves = [(v, k) for k, v in self.rates.items()]
        valves.sort(reverse=True)
        # Make each actor visit every other valve, from highest to lowest
        path1 = [valves[v][1] for v in range(0, len(valves), 2)]
        path2 = [valves[v][1] for v in range(1, len(valves), 2)]
        # Count cost of each path
        def take_path(path):
            cost = 0
            time = time_left
            steps = 0
            pos = 'AA'
            for step in path:
                time_cost = self.distances[pos][step] + 1
                if time_cost >= time:
                    # ran out of time
                    break
                pos = step
                time -= time_cost
                cost += self.rates[step] * time
                steps += 1
            return cost, steps
        cost1, steps1 = take_path(path1)
        cost2, steps2 = take_path(path2)
        path1 = path1[:steps1]
        path2 = path2[:steps2]
        actor1 = Actor(pos=path1[-1], time_left=0, stopped=True, path=path1)
        actor2 = Actor(pos=path2[-1], time_left=0, stopped=True, path=path2)
        return State(
            actors = [actor1, actor2],
            value = cost1 + cost2,
            valves_turned = [],
            valves_unturned = [],
        )


    def with_elephant_astar(self, time_left):
        a = Actor(pos='AA', time_left=time_left, stopped=False, path=['AA'])
        b = Actor(pos='AA', time_left=time_left, stopped=False, path=['AA'])
        state = State(
            actors=[a,b],
            value=0,
            valves_turned=['AA'],
            valves_unturned=[k for k in self.rates.keys() if k != 'AA']
        )
        q = [(-10000, state)]

        def estimate_value(state):
            values = sorted([self.rates[k] for k in state.valves_unturned], reverse=True)
            maxtime = max(
                state.actors[0].time_left if not state.actors[0].stopped else 0,
                state.actors[1].time_left if not state.actors[1].stopped else 0
            )
            estimate = state.value
            for v in values:
                estimate += max(0, maxtime - 1) * v
                maxtime -= 2
            return estimate

        best_state = self.find_some_solution(time_left)
        counter = 0
        while q:
            # Take the most promising state from the priority queue
            est, state = heapq.heappop(q)
            est = -est

            counter += 1
            if counter % 10000 == 0:
                print(f"{counter}: best_state {best_state.value if best_state is not None else 0}, head_est {est}, q size {len(q)}")

            if est < best_state.value:
                # The (over)estimate of the value of the current state is worse
                # than the value of the best solution so far. No need to go further,
                # the best_state is globally best
                break

            if not state.valves_unturned:
                # Found solution
                if state.value > best_state.value:
                    best_state = state
                continue

            # First actor's move
            active_actor = 0
            actor = state.actors[active_actor]
            if not actor.stopped and actor.time_left > 2:
                # A move can be:
                # * move to another unturned valve and turn it
                for i, valve in enumerate(state.valves_unturned):
                    distance = self.distances[actor.pos][valve]
                    if actor.time_left <= distance + 1:
                        # 'distance' minutes to get to the valve
                        # + 1 minute to turn the valve
                        # + 1 minute for the valve to have any effect
                        # -> it only makes sense to go to the valve if we have more than
                        # 'distance + 1' minutes left.
                        continue
                    new_actor = Actor(
                        pos = valve,
                        time_left = actor.time_left - distance - 1,
                        stopped = False,
                        path = actor.path + [valve]
                    )
                    value = self.rates[valve] * new_actor.time_left
                    new_state = State(
                        actors = [new_actor, state.actors[1]],
                        value = state.value + value,
                        valves_turned = state.valves_turned + [valve],
                        valves_unturned = state.valves_unturned[:i] + state.valves_unturned[i+1:]
                    )
                    new_est = estimate_value(new_state)
                    if new_est > best_state.value:
                        # only push states that have a chance of being better than the current best
                        heapq.heappush(q, (-new_est, new_state))

                # The following is actually not necessary
                # We don't need the stopped property, because the code does
                # (move + turn valve); not (turn valve + move), so it is possible
                # to just go to a valve, turn it, and stop there.
                """
                # * do nothing, stop for the rest of the time
                #   this is not permitted to be the first move of the first actor
                if len(state.values_turned) > 1:
                    new_actor = Actor(
                        pos = actor.pos,
                        time_left = 0,
                        stopped = True,
                        path = actor.path
                    )
                    new_state = State(
                        actors = [new_actor, state.actors[1]],
                        value = state.value,
                        valves_unturned = state.valves_unturned
                    )
                    # Nothing moved, so the estimated value of the new state is the same as
                    # the estimated value of the current state
                    heapq.heappush(-est, new_state)
                """

            # Unless this is the very first turn, which is always taken by the first
            # actor only (to break the symmetry of the actors, otherwise we would have
            # two sets of identical states just with swapped actors), allow the second
            # actor to make a move
            if len(state.valves_turned) > 1:
                active_actor = 1
                actor = state.actors[active_actor]
                if not actor.stopped and actor.time_left > 2:
                    # A move can be:
                    # * move to another unturned valve and turn it
                    for i, valve in enumerate(state.valves_unturned):
                        distance = self.distances[actor.pos][valve]
                        if actor.time_left <= distance + 1:
                            # 'distance' minutes to get to the valve
                            # + 1 minute to turn the valve
                            # + 1 minute for the valve to have any effect
                            # -> it only makes sense to go to the valve if we have more than
                            # 'distance + 1' minutes left.
                            continue
                        new_actor = Actor(
                            pos = valve,
                            time_left = actor.time_left - distance - 1,
                            stopped = False,
                            path = actor.path + [valve]
                        )
                        value = self.rates[valve] * new_actor.time_left
                        new_state = State(
                            actors = [state.actors[0], new_actor],
                            value = state.value + value,
                            valves_turned = state.valves_turned + [valve],
                            valves_unturned = state.valves_unturned[:i] + state.valves_unturned[i+1:]
                        )
                        new_est = estimate_value(new_state)
                        if new_est > best_state.value:
                            # only push states that have a chance of being better than the current best
                            heapq.heappush(q, (-new_est, new_state))

        assert best_state is not None, "solution not found"
        best_path = best_state.actors[0].path + [x + 'e' for x in best_state.actors[1].path]
        return best_state.value, best_path


"""
    def find_best_value_with_help(self, start, elephant, time_left, elephant_time, turned_valves):
        # Problem: who has more time is the one who moves next. However, because both are at
        # different positions, the one who moves first might have a longer distance to their
        # destination than the other one would.

        if time_left <= 0 and elephant_time <= 0:
            return 0, ''

        if elephant_time > time_left:
            elephants_move = True
            pos = elephant
            time = elephant_time
        else:
            elephants_move = False
            pos = start
            time = time_left

        # value of turning the valve at the current position, costing 1 time
        turn_value = self.rates[pos] * (time - 1)
        if turn_value > 0:
            time -= 1
        best_value = turn_value
        best_path = ''

        # try proceeding with turning the current valve
        dist = self.distances[pos]
        for n in dist.keys():
            if n in turned_valves or dist[n] > time:
                continue
            turned_valves.add(n)
            if elephants_move:
                path_value, path = self.find_best_value_with_help(start, n, time_left, time - dist[n], turned_valves)
            else:
                path_value, path = self.find_best_value_with_help(n, elephant, time - dist[n], elephant_time, turned_valves)
            if turn_value + path_value > best_value:
                best_path = path
                best_value = turn_value + path_value
            turned_valves.remove(n)

        current_pos = f"[{start}({time_left}) {elephant}({elephant_time}){' e' if elephants_move else ''}], "
        return best_value, current_pos + best_path
"""


def part1(input):
    full_map = Map.make(input.get_valid_lines())
    #print(full_map)
    map = SimplerMap.simplify(full_map)
    #print(map)
    value, path = map.find_best_value('AA', 30, set())
    print(path)
    return value


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    full_map = Map.make(input.get_valid_lines())
    map = SimplerMap.simplify(full_map)
    print(map)
    # Takes about 6 hours:
    value, path = map.find_best_value_with_help('AA', 'AA', 26, 26, set(['AA']), False, False, 0, len(map.rates)-1, sum(map.rates.values()))
    # Runs out of memory:
    #value, path = map.with_elephant_astar(26)
    print(path)
    return value


e.run_tests(2, part2)
e.run_main(2, part2)

"""
AA, DD, BB, JJ, HH, EE, CC,
Test 0 SUCCEEDED: result 1651
     0 13  2 20  3 22 21
    AA BB CC DD EE HH JJ
AA   0  1  2  1  2  5  2
BB   1  0  1  2  3  6  3
CC   2  1  0  1  2  5  4
DD   1  2  1  0  1  4  3
EE   2  3  2  1  0  3  4
HH   5  6  5  4  3  0  7
JJ   2  3  4  3  4  7  0
[AA(26) AA(26)], [DD(25) AA(26)], [HH(20) AA(26)], [EE(16) AA(26)], [EE(15) AA(26) e], [EE(15) JJ(24) e], [EE(15) BB(20) e], [EE(15) CC(18) e],
Test 0 SUCCEEDED: result 1707
     0 10 12  7 15 25 13  3  9  8 23 21 17 16 18 19
    AA EU FF KF MH NQ NT NW QL QM QW SX TZ VC XY ZU
AA   0  7  5  3  3  8  3  3  5  3  5  7  7  7  6  5
EU   7  0  3  5 10  5  7  7  2  4 12  2  4 13  3 10
FF   5  3  0  2  7  3  4  5  5  5  9  2  7 10  2  7
KF   3  5  2  0  5  5  2  3  5  3  7  4  7  8  4  5
MH   3 10  7  5  0 10  3  3  8  6  2  9 10  4  9  2
NQ   8  5  3  5 10  0  7  8  7  5 12  3  9 13  2 10
NT   3  7  4  2  3  7  0  2  7  5  5  6  9  6  6  3
NW   3  7  5  3  3  8  2  0  5  3  5  7  7  7  6  5
QL   5  2  5  5  8  7  7  5  0  2 10  4  2 12  5 10
QM   3  4  5  3  6  5  5  3  2  0  8  6  4 10  3  8
QW   5 12  9  7  2 12  5  5 10  8  0 11 12  2 11  2
SX   7  2  2  4  9  3  6  7  4  6 11  0  6 12  3  9
TZ   7  4  7  7 10  9  9  7  2  4 12  6  0 14  7 12
VC   7 13 10  8  4 13  6  7 12 10  2 12 14  0 12  3
XY   6  3  2  4  9  2  6  6  5  3 11  3  7 12  0  9
ZU   5 10  7  5  2 10  3  5 10  8  2  9 12  3  9  0
[AA(26) AA(26)], [MH(23) AA(26)], [QW(20) AA(26)], [VC(17) AA(26)], [ZU(13) AA(26)], [NT(9) AA(26)], [KF(6) AA(26)], [FF(3) AA(26)], [FF(2) AA(26) e], [FF(2) QM(23) e], [FF(2) XY(19) e], [FF(2) NQ(16) e], [FF(2) SX(12) e], [FF(2) EU(9) e], [FF(2) QL(6) e], [FF(2) TZ(3) e],
Day 16 Part 2: 2679

real    380m58.707s
user    380m57.117s
sys     0m0.661s
"""
