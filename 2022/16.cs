using System.Diagnostics;
using System.Text.RegularExpressions;

class Day16
{
    const string start = "AA";

    private Graph graph;

    public Day16(string inputText)
    {
        var nodes = inputText.Split("\n").Where(x => x.Length > 0).Select(line => new SimpleNode(line));
        graph = new Graph(nodes);
        graph.print();
    }

    private class Workload
    {
        public int value { get; set; }
        public int workers { get; set; }
        public int valveConfig { get; set; }
        public int lastSetAdded { get; set; }
        public List<int> sets { get; set; }
        public Workload(int value, int workers, int valveConfig,  int lastSetAdded, List<int> sets)
        {
            this.value = value;
            this.workers = workers;
            this.valveConfig = valveConfig;
            this.lastSetAdded = lastSetAdded;
            this.sets = sets;
        }
    }

    internal int solve(int numElephants, int time)
    {
        (var setDict, var valveConfig) = bestOucomePerValveSet(time);
        var sets = setDict.ToList();
        var startValveConfig = valveConfig.StartConfig();

        Console.WriteLine($"{sets.Count} sets");

        int maxWorkers = numElephants + 1;
        var queue = new Queue<Workload>();
        queue.Enqueue(new Workload(0, 0, startValveConfig, -1, new List<int>()));
        Workload best = new Workload(0, 0, 0, -1, new List<int>());
        while (queue.Count > 0)
        {
            var workload = queue.Dequeue();
            if (best.value < workload.value)
            {
                best = workload;
            }
            if (workload.workers < maxWorkers)
            {
                for (int i = workload.lastSetAdded + 1; i < sets.Count; i++)
                {
                    var set = sets[i].Key;
                    // All configurations include the starting valve, so the starting valve is the common element in all the sets
                    if ((workload.valveConfig & set) == startValveConfig)
                    {
                        var newValue = workload.value + sets[i].Value;
                        var newSets = workload.sets.ToList();
                        newSets.Add(set);
                        queue.Enqueue(new Workload(
                            newValue,
                            workload.workers + 1,
                            workload.valveConfig | set,
                            i,
                            newSets)
                        );
                    }
                }
            }
        }

        Console.WriteLine($"Value = {best.value}, workers = {best.workers}, sets = {String.Join(", ", best.sets.Select(x=>x.ToString()))}");
        return best.value;
        // FIXME: return a full reconstructed path, not just a number
    }

    internal int part1()
    {
        return solve(0, 30);
    }

    internal int part2()
    {
        return solve(1, 26);
    }

    private class ValveConfig
    {
        private List<string> m_sortedValves;
        private Dictionary<string, int> m_valveIndexes;
        public int config { get; private set; }

        public ValveConfig(IEnumerable<string> valves)
        {
            m_sortedValves = valves.ToList();
            m_sortedValves.Sort();

            // We'll be using an int as a bitset.
            // Everything will definitely be fine if the number of bits required is less than 32.
            Debug.Assert(m_sortedValves.Count < 32);

            config = 0;
            m_valveIndexes = new Dictionary<string, int>();
            for (int i = 0; i < m_sortedValves.Count; i++)
            {
                m_valveIndexes[m_sortedValves[i]] = i;
            }
        }

        private ValveConfig(List<string> sortedValues, Dictionary<string, int> valveIndexes, int configValue, string newValve)
        {
            m_sortedValves = sortedValues;
            m_valveIndexes = valveIndexes;
            config = configValue;
            var newIndex = m_valveIndexes[newValve];
            config |= 1 << newIndex;
        }

        public ValveConfig Add(string valve)
        {
            return new ValveConfig(m_sortedValves, m_valveIndexes, config, valve);
        }

        public bool Turned(string valve)
        {
            var valveIndex = m_valveIndexes[valve];
            return (config & (1 << valveIndex)) > 0;
        }

        // Bitset config representing only the starting valve
        public int StartConfig()
        {
            var valveIndex = m_valveIndexes[start];
            return 1 << valveIndex;
        }
    }

    private class VisitState
    {
        public string valve { get; set; }
        public ValveConfig turnedValves { get; set; }
        public int steam { get; set; }
        public int timeLeft { get; set; }

        public VisitState(string valve, ValveConfig turnedValves, int steam, int timeLeft)
        {
            this.valve = valve;
            this.turnedValves = turnedValves;
            this.steam = steam;
            this.timeLeft = timeLeft;
        }
    }

    private Tuple<Dictionary<int, int>, ValveConfig> bestOucomePerValveSet(int time)
    {
        var bestOutcome = new Dictionary<int, int>();
        var queue = new Queue<VisitState>();
        var emptyValves = new ValveConfig(graph.valveFlow.Keys);
        queue.Enqueue(new VisitState(start, emptyValves.Add(start), 0, time));
        while (queue.Count > 0)
        {
            var state = queue.Dequeue();
            if (!bestOutcome.ContainsKey(state.turnedValves.config) || bestOutcome[state.turnedValves.config] < state.steam)
            {
                bestOutcome[state.turnedValves.config] = state.steam;
            }
            foreach (var next in graph.valveFlow.Keys)
            {
                if (state.turnedValves.Turned(next))
                {
                    continue;
                }
                var dist = graph.distances[Tuple.Create(state.valve, next)];
                var remTime = state.timeLeft - dist - 1;
                if (remTime <= 0)
                {
                    continue;
                }
                var extraSteam = graph.valveFlow[next] * remTime;
                queue.Enqueue(new VisitState(next, state.turnedValves.Add(next), state.steam + extraSteam, remTime));
            }
        }
        // emptyValves provides the ordering of the valves in the bitset
        return Tuple.Create(bestOutcome, emptyValves);
    }

    private class SimpleNode
    {
        private static Regex rx = new Regex(@"Valve (?<valve>..) has flow rate=(?<flow>\d+); tunnels? leads? to valves? (?<next>.*)", RegexOptions.Compiled);

        public string valveName { get; private set; }
        public int flow { get; private set; }
        public List<string> connections { get; private set; }

        public SimpleNode(string line)
        {
            var match = rx.Match(line);
            Debug.Assert(match.Success);
            var groups = match.Groups;
            valveName = groups["valve"].Value;
            flow = int.Parse(groups["flow"].Value);
            connections = groups["next"].Value.Split(", ").ToList();
        }
    }

    private class Graph
    {
        public Dictionary<string, int> valveFlow { get; private set; } = new Dictionary<string, int>();
        public Dictionary<Tuple<string, string>, int> distances { get; private set; } = new Dictionary<Tuple<string, string>, int>();

        public Graph(IEnumerable<SimpleNode> nodes)
        {
            // Floyd-Warshall algorithm to find distances between all pairs of nodes.
            // Each plain edge has weight 1.
            var allDist = new Dictionary<Tuple<string, string>, int>();
            // Set shortest distance between all connected nodes to 1, and from each node to itself to 0
            foreach (var node in nodes)
            {
                if (node.flow > 0 || node.valveName == start)
                {
                    // In valveFlow, we collect the valves that have flow > 0, and the special case "AA"
                    valveFlow.Add(node.valveName, node.flow);
                }
                foreach (var next in node.connections) {
                    allDist.Add(Tuple.Create(node.valveName, next), 1);
                }
                allDist.Add(Tuple.Create(node.valveName, node.valveName), 0);
            }
            // For each intermediate node K
            foreach (var nodeK in nodes)
            {
                // For each start node I
                foreach (var nodeI in nodes)
                {
                    var iTok = Tuple.Create(nodeI.valveName, nodeK.valveName);
                    if (!allDist.ContainsKey(iTok)) {
                        continue;
                    }
                    var ikDistance = allDist[iTok];
                    // For each destination node J
                    foreach (var nodeJ in nodes)
                    {
                        var iToj = Tuple.Create(nodeI.valveName, nodeJ.valveName);
                        var kToj = Tuple.Create(nodeK.valveName, nodeJ.valveName);
                        if (!allDist.ContainsKey(kToj))
                        {
                            continue;
                        }
                        // If (i->k->j) is shorter than (i->j), make (i->k->j) the shortes path between i and j
                        var newDist = ikDistance + allDist[kToj];
                        if (!allDist.ContainsKey(iToj) || allDist[iToj] > newDist)
                        {
                            allDist[iToj] = newDist;
                        }
                    }
                }
            }

            // We only care about the nodes from valveFlow, discard all other nodes
            foreach (var nodeFrom in valveFlow.Keys)
            {
                foreach (var nodeTo in valveFlow.Keys)
                {
                    var pair = Tuple.Create(nodeFrom, nodeTo);
                    distances[pair] = allDist[pair];
                }
            }
        }

        public void print()
        {
            var keys = valveFlow.Keys.ToList();
            keys.Sort();

            Console.WriteLine($"[Graph nodes: {valveFlow.Count}]");

            string flows = "  ";
            string headings = "  ";
            foreach (var key in keys)
            {
                flows += $"  {valveFlow[key], 2}";
                headings += $"  {key,2}";
            }
            Console.WriteLine(flows);
            Console.WriteLine(headings);
            foreach (var valve in keys)
            {
                var line = valve;
                foreach (var nodeTo in keys)
                {
                    line += $"  {distances[Tuple.Create(valve, nodeTo)],2}";
                }
                Console.WriteLine(line);
                //Console.WriteLine($"{valve}  {String.Join("  ", valveFlow.Keys.Select(k => distances[Tuple.Create(nodeFrom, k)].ToString()))}]");
            }
        }
    }
}

