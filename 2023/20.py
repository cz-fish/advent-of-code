#!/usr/bin/python3.8

from pyaoc import Env
from collections import defaultdict, deque
from pyaoc import integers


e = Env(20)
e.T("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 32000000, None)

e.T("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""", 11687500, None)

FLIP = '%'
CONJ = '&'
SPECIAL = ' '

def parse_input(input):
    modules = {}
    reverse = defaultdict(list)
    for ln in input.get_valid_lines():
        left, right = ln.split(" -> ")
        if left.startswith(FLIP):
            type = FLIP
            name = left[1:]
        elif left.startswith(CONJ):
            type = CONJ
            name = left[1:]
        else:
            type = SPECIAL
            name = left
        assert name not in modules
        dests = right.split(", ")
        for d in dests:
            assert name not in reverse[d]
            reverse[d].append(name)
        modules[name] = (type, dests)
    for r in reverse.keys():
        if r not in modules:
            modules[r] = ((SPECIAL, []))
    return modules, reverse


LOW = 0
HIGH = 1


def push_button_and_count_signals(modules, reverse, state):
    q = deque()
    highs = 0
    lows = 0
    q.append(('broadcaster', LOW))
    #count = 0
    while q:
        module, pulse = q.popleft()
        ###
        #print(count, module, pulse)
        #count += 1
        #if count > 10:
        #    break
        ###
        if pulse == HIGH:
            highs += 1
        else:
            lows += 1
        if module not in modules:
            # dummy output module
            continue
        type, output = modules[module]
        stop = False
        if type == FLIP:
            # high pulse ignored, low pulse flips
            if pulse == LOW:
                old_state = state[module]
                new_state = LOW if old_state == HIGH else HIGH
                state[module] = new_state
            else:
                stop = True
        elif type == CONJ:
            # if all inputs are high, outputs low, otherwise outputs high
            input_is_high = True
            for p in reverse[module]:
                if state[p] == LOW:
                    input_is_high = False
                    break
            new_state = LOW if input_is_high else HIGH
            state[module] = new_state
        elif type == SPECIAL:
            # broadcaster
            new_state = pulse

        if not stop:
            for d in output:
                q.append((d, new_state))
    return lows, highs


def part1(input):
    modules, reverse = parse_input(input)
    state = {
        mod: LOW for mod in modules.keys()
    }
    tot_low = 0
    tot_high = 0
    for i in range(1000):
        lows, highs = push_button_and_count_signals(modules, reverse, state)
        tot_low += lows
        tot_high += highs
    return tot_low * tot_high


e.run_tests(1, part1)
e.run_main(1, part1)


def print_graph(modules, reverse):
    # Write a .dot file that can be rendered by graphviz' dot program
    start = "broadcaster"
    target = "rx"
    inverters = []
    nands = []
    with open('20.dot', 'wt') as f:
        print("digraph {", file=f)
        for name, info in modules.items():
            type, edges = info
            in_edges = len(reverse[name])
            if type == FLIP:
                attr = "shape=invtriangle"
                if in_edges == 1:
                    attr += ",fillcolor=gray92"
                else:
                    attr += ",fillcolor=yellow"
                if len(edges) == 1:
                    attr += ",style=dashed"
                else:
                    attr += ",style=filled"
            elif type == CONJ:
                if in_edges == 1:
                    attr = "shape=ellipse,color=cyan,style=filled"
                    inverters.append(name)
                else:
                    attr = "shape=parallelogram,color=green,style=filled"
                    nands.append(name)
            else:
                if name == target:
                    attr = "shape=box,color=red"
                else:
                    attr = "shape=box"
            print(f"    {name} [{attr}]", file=f)
            for d in edges:
                print(f"    {name} -> {d}", file=f)
        print(f"    {{ rank=source; {start} }}", file=f)
        print(f"    {{ rank=sink; {target} }}", file=f)
        print(f"    {{ rank=same; {', '.join(inverters)} }}", file=f)
        #print(f"    {{ rank=same; {', '.join(nands)} }}", file=f)
        #print(f"    {{ rank=3; {', '.join(modules[start][1])} }}", file=f)
        print("}", file=f)


def find_branch_period(start, modules):
    # Start node is a flipflop
    assert modules[start][0] == FLIP
    # It always outputs to a conjunction, that helps us find that conjunction
    conj = None
    for d in modules[start][1]:
        if modules[d][0] == CONJ:
            assert conj is None
            conj = d
    assert conj is not None
    # `conj` is the conjunction for the current branch. Flipflops that send to
    # it are the important bits
    value = 0
    bit_value = 1
    node = start
    while node:
        next_node = None
        for d in modules[node][1]:
            if d == conj:
                # the node `node` is an important bit
                value += bit_value
            else:
                assert next_node is None
                next_node = d
        bit_value *= 2
        node = next_node
    return value


def part2(input):
    modules, reverse = parse_input(input)
    #print_graph(modules, reverse)

    """
    Analysis of the graph
    * Broadcaster sends LOW to 4 separate branches
    * Each branch is a 12 bit counter and a conjuction. Some of those 12  bits contribute to the conjunction
    * The result of each of the branches is a LOW if all the bits that contribute to the conjunction are HIGH
    * When the conjunction of a branch becomes LOW (all its inputs are HIGH), it will do two things:
       * send a LOW to an invertor (which converts it to HIGH) and to a finial conjunction that sends to node 'rx'
       * send a LOW to all the bits of the counter that don't contribute to the conjunction. All of these bits
         are LOW at that moment. The LOW signal from the conjunction will flip them all to HIGH, so then all the
         bits of the counter will be HIGH. Finally, a last LOW to the first bit of the counter resets all the
         bit flipflops back to 0, and that completes a cycle for that particular branch
    * The four different branches have 4 different periods (that all happen to be prime numbers)
    * For the final conjunction to fire LOW to node `rx`, all 4 branches have to produce LOW at the same cycle,
      which happens after the lowest common multiple of all the 4 periods (but because they are co-prime, it's the
      same as just a multiple of those 4 periods).
    * The period of each branch is determined by the configuration of which bits contribute to the conjunction.
       * After each button press, the counter is incremented by 1 (the lowest bit is flipped. If it's flipped to 0, it
         will then cascade flip the next bit, and so on).
       * The length of the period is the sum of the powers of two of the order of bit flipflops that send output to
         the conjunction.
    """

    # walk the modules graph, identify the branches. For each branch find the contributing bits, and use
    # those to calculate the period. The calculate the LCM of all the periods.
    branch_starts = modules['broadcaster'][1]
    periods = []
    for start in branch_starts:
        periods.append(find_branch_period(start, modules))
    assert len(periods) > 0
    result = periods[0]
    for period in periods:
        result = integers.Integers.lcm(result, period)
    return result


e.run_main(2, part2)
