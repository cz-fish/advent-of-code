using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace AoC2022
{
    internal class Day19
    {
        public long totalStatesProbed = 0;

        internal enum Material
        {
            Ore = 0,
            Clay = 1,
            Obsidian = 2,
            Geode = 3,
        }

        internal class Materials
        {
            public int ore { get; private set; }
            public int clay { get; private set; }
            public int obsidian { get; private set; }
            public int geode { get; private set; }

            public Materials(int ore, int clay, int obsidian, int geode)
            {
                this.ore = ore;
                this.clay = clay;
                this.obsidian = obsidian;
                this.geode = geode;
            }

            public int this[Material i]
            {
                get
                {
                    return i switch
                    {
                        Material.Ore => ore,
                        Material.Clay => clay,
                        Material.Obsidian => obsidian,
                        Material.Geode => geode,
                        _ => throw new IndexOutOfRangeException(),
                    };
                }
                set
                {
                    switch (i)
                    {
                        case Material.Ore: ore = value; break;
                        case Material.Clay: clay = value; break;
                        case Material.Obsidian: obsidian = value; break;
                        case Material.Geode: geode = value; break;
                        default: throw new IndexOutOfRangeException();
                    }
                }
            }

            public Materials AddOne(Material material)
            {
                var result = new Materials(ore, clay, obsidian, geode);
                result[material] += 1;
                return result;
            }

            public override string ToString()
            {
                return $"[Or{ore}, Cl {clay}, Ob {obsidian}, Ge {geode}]";
            }
        }

        internal class Blueprint
        {
            public int index {get; private set;}

            public Materials ore_cost { get; private set; }
            public Materials clay_cost { get; private set; }
            public Materials obsidian_cost { get; private set; }
            public Materials geode_cost { get; private set; }

            public Blueprint(string line)
            {
                var numbers = Regex.Matches(line, @"\d+").Select(w => int.Parse(w.Value)).ToList();
                Debug.Assert(numbers.Count == 7);
                index = numbers[0];
                ore_cost = new Materials(numbers[1], 0, 0, 0);
                clay_cost = new Materials(numbers[2], 0, 0, 0);
                obsidian_cost = new Materials(numbers[3], numbers[4], 0, 0);
                geode_cost = new Materials(numbers[5], 0, numbers[6], 0);
            }

            public Materials this[Material type]
            {
                get
                {
                    return type switch
                    {
                        Material.Ore => ore_cost,
                        Material.Clay => clay_cost,
                        Material.Obsidian => obsidian_cost,
                        Material.Geode => geode_cost,
                        _ => throw new IndexOutOfRangeException(),
                    };
                }
            }

            // Return maximal amount of material of type 'type' to build any of the kinds of robot.
            public int maxMaterialCost(Material type)
            {
                var matArray = (Material[]) Enum.GetValues(typeof(Material));
                return matArray.Select(mat => this[mat][type]).Max();
            }

            public override string ToString()
            {
                return $"[Blueprint {index}. Robot costs: ore {ore_cost}, clay {clay_cost}, obsidian {obsidian_cost}, geode {geode_cost}]";
            }
        }

        private List<Blueprint> blueprints;

        public Day19(string input)
        {
            this.blueprints = input.Split("\n")
                                   .Where(line => line.Length > 0)
                                   .Select(line => new Blueprint(line))
                                   .ToList();
        }

        internal int part1()
        {
            const int TimePart1 = 24;
            return blueprints.Select(blueprint => evaluateBlueprint(blueprint, TimePart1) * blueprint.index)
                             .Sum();
        }

        internal int part2()
        {
            const int TimePart2 = 32;
            const int BlueprintCount = 3;
            return blueprints.Take(BlueprintCount)
                             .Select(blueprint => evaluateBlueprint(blueprint, TimePart2))
                             .Aggregate(1, (val, total) => total * val);
        }

        private class ProductionState {
            public int timeLeft { get; set; }
            public Materials resource { get; set; }
            public Materials robots { get; set; }

            public ProductionState(int time)
            {
                timeLeft = time;
                resource = new Materials(0, 0, 0, 0);
                robots = new Materials(1, 0, 0, 0);
            }

            public ProductionState(int time, Materials resource, Materials robots)
            {
                timeLeft = time;
                this.resource = resource;
                this.robots = robots;
            }
        }


        internal int evaluateBlueprint(Blueprint b, int time)
        {
            // We can use a queue or a stack for open states. It seems that using a queue reduces
            // the number of states that we need to visit to ~85% of those needed when using a stack,
            // at least on the given input. So we'll use the queue.
            var queue = new Queue<ProductionState>();
            queue.Enqueue(new ProductionState(time));

            int mostGeodes = 0;

            var maxRobotsNeeded = new Materials(
                b.maxMaterialCost(Material.Ore),
                b.maxMaterialCost(Material.Clay),
                b.maxMaterialCost(Material.Obsidian),
                b.maxMaterialCost(Material.Geode)
            );

            while (queue.Count > 0)
            {
                totalStatesProbed++;
                var state = queue.Dequeue();
                if (state.resource.geode > mostGeodes)
                {
                    mostGeodes = state.resource.geode;
                }
                if (state.timeLeft <= 1) {
                    // No time to build anything else; end state
                    continue;
                }

                // Prune states that are not perspective - a real time saver!
                // If we were to build a geode robot from now on in every minute, how much could
                // we possibly harvest?
                var potential = (state.timeLeft - 1) * (state.timeLeft - 1 + 1) / 2;
                if (state.resource.geode + potential <= mostGeodes)
                {
                    // No point continuing with this path; it cannot beat the current best
                    continue;
                }

                foreach (Material buildNext in Enum.GetValues(typeof(Material)))
                {
                    // Is it possible to build this material robot?
                    int timeToBuild = 0;
                    bool impossibleToBuild = false;
                    var cost = b[buildNext];
                    foreach (Material resource in Enum.GetValues(typeof(Material)))
                    {
                        if (cost[resource] > 0)
                        {
                            if (state.robots[resource] == 0)
                            {
                                // impossible to build next; we don't have the right dependency robot yet
                                impossibleToBuild = true;
                                break;
                            }
                            var resourceNeeded = Math.Max(cost[resource] - state.resource[resource], 0);
                            var timeNeeded = (resourceNeeded + state.robots[resource] - 1) / state.robots[resource]; // rounded up to int
                            timeToBuild = Math.Max(timeToBuild, timeNeeded);
                        }
                    }
                    // +1 for the time to actually build the robot
                    timeToBuild += 1;
                    // Time needs to be strictly greater, otherwise we'd just build the robot but not have time to use it
                    if (impossibleToBuild || timeToBuild > state.timeLeft)
                    {
                        // will not build this robot type next
                        continue;
                    }

                    // At this point, it is possible to build the robot of type 'buildNext', and it would take 'timeToBuild'.
                    // But is it useful to build that type? (It is always useful to build a geode robot)
                    if (buildNext != Material.Geode)
                    {
                        if (state.robots[buildNext] >= maxRobotsNeeded[buildNext])
                        {
                            // We already have enough robots of this type that we will ever need
                            continue;
                        }
                        // It doesn't make sense to build anything else than a geode robot if it's our last one
                        if (state.timeLeft <= 2)
                        {
                            continue;
                        }
                    }

                    // It is possible and might make sense to build this robot. Let's build it.

                    // How much of each material will be harvested while we're waiting to build the robot.
                    // Geodes are counted differently, because we're not consuming them. They are booked at
                    // the time when we complete building the robot
                    var resourcesLeft = new Materials(
                        state.resource.ore + state.robots.ore * timeToBuild - cost.ore,
                        state.resource.clay + state.robots.clay * timeToBuild - cost.clay,
                        state.resource.obsidian + state.robots.obsidian * timeToBuild - cost.obsidian,
                        state.resource.geode
                    );
                    var newRobots = state.robots.AddOne(buildNext);
                    var newTimeLeft = state.timeLeft - timeToBuild;

                    if (buildNext == Material.Geode)
                    {
                        resourcesLeft[Material.Geode] += newTimeLeft;
                    }

                    queue.Enqueue(new ProductionState(newTimeLeft, resourcesLeft, newRobots));
                }
            }

            Console.WriteLine($"Blueprint {b.index} -> most geodes {mostGeodes}");

            return mostGeodes;
        }
    }
}
