#include <array>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

struct Blueprint {
    int ore_ore;
    int clay_ore;
    int obsidian_ore;
    int obsidian_clay;
    int geode_ore;
    int geode_obsidian;
};

std::ostream& operator<<(std::ostream& o, Blueprint const& bp)
{
    o << "[\n"
      << "  ore_robot: " << bp.ore_ore << " ore\n"
      << "  clay_robot: " << bp.clay_ore << " ore\n"
      << "  obsidian_robot: " << bp.obsidian_ore << " ore, " << bp.obsidian_clay << " clay\n"
      << "  geode_robot: " << bp.geode_ore << " ore, " << bp.geode_obsidian << " obsidian\n"
      << "]";
    return o;
}

std::vector<Blueprint> readBlueprints(std::ifstream& input)
{
    std::vector<Blueprint> blueprints;
    std::array<char, 200> lineBuf;

    while (!input.eof()) {
        input.getline(&lineBuf[0], 200);
        std::string line(&lineBuf[0], std::strlen(&lineBuf[0]));
        if (line.size() == 0) {
            continue;
        }

        auto reader = std::stringstream{line};
        std::string dummy;
        // Blueprint 30: Each ore robot costs 4 ore. Each clay robot costs 4 ore.
        // Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs
        // 4 ore and 19 obsidian.
        int ore_ore;
        int clay_ore;
        int obsidian_ore;
        int obsidian_clay;
        int geode_ore;
        int geode_obsidian;
        reader >> dummy >> dummy >> dummy >> dummy >> dummy >> dummy >> ore_ore
               >> dummy >> dummy >> dummy >> dummy >> dummy >> clay_ore
               >> dummy >> dummy >> dummy >> dummy >> dummy >> obsidian_ore
               >> dummy >> dummy >> obsidian_clay
               >> dummy >> dummy >> dummy >> dummy >> dummy >> geode_ore
               >> dummy >> dummy >> geode_obsidian;
        blueprints.push_back(Blueprint{
            ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian});
    }

    return blueprints;
}

struct State {
    int ore;
    int clay;
    int obsidian;
    int geode;
    int ore_robot;
    int clay_robot;
    int obsidian_robot;
    int geode_robot;
};

enum NewRobot {
    NONE = 0,
    ORE = 1,
    CLAY = 2,
    OBSIDIAN = 3,
    GEODE = 4
};

void add_state(NewRobot which, State const& state, Blueprint const& bp, std::vector<State>& list)
{
    int add_ore = 0;
    int add_clay = 0;
    int add_obsidian = 0;
    int add_geode = 0;
    int cost_ore = 0;
    int cost_clay = 0;
    int cost_obsidian = 0;
    switch (which) {
    case NewRobot::ORE:
        add_ore = 1;
        cost_ore = bp.ore_ore;
        break;
    case NewRobot::CLAY:
        add_clay = 1;
        cost_ore = bp.clay_ore;
        break;
    case NewRobot::OBSIDIAN:
        add_obsidian = 1;
        cost_ore = bp.obsidian_ore;
        cost_clay = bp.obsidian_clay;
        break;
    case NewRobot::GEODE:
        add_geode = 1;
        cost_ore = bp.geode_ore;
        cost_obsidian = bp.geode_obsidian;
        break;
    }
    list.push_back({
        state.ore + state.ore_robot - cost_ore,
        state.clay + state.clay_robot - cost_clay,
        state.obsidian + state.obsidian_robot - cost_obsidian,
        state.geode + state.geode_robot,
        state.ore_robot + add_ore,
        state.clay_robot + add_clay,
        state.obsidian_robot + add_obsidian,
        state.geode_robot + add_geode
    });
}


int geodesFromBlueprint(Blueprint const& bp, int const time)
{
    bool part2_pruning = (time == 32);
    int const clay_robot_limit = part2_pruning? 10 : 8;
    int const ore_robot_limit = part2_pruning? 10: 7;
    int const obsidian_robot_limit = part2_pruning? 10: 20;
    std::vector<State> current_states;
    std::vector<State> new_states;
    current_states.push_back({0, 0, 0, 0, 1, 0, 0, 0});
    int geode_robot_count = 0;
    int obsidian_robot_count = 0;
    for (int minute = 0; minute < time; ++minute) {
        //std::cout << "minute " << minute << ", states " << current_states.size() << std::endl;
        new_states.clear();
        for (auto const& state : current_states) {
            /* Unsafe optimization: If we already know a state with N geode robots where N is
             * more than 1 higher than the current state's geode robots, then prune that branch. */
            if (part2_pruning) {
                if (state.geode_robot > geode_robot_count) {
                    geode_robot_count = state.geode_robot;
                }
                if (state.geode_robot < geode_robot_count - 1) {
                    continue;
                }

                /* Follow-up unsafe optimization - do the same on obsidian robots */

                if (state.obsidian_robot > obsidian_robot_count) {
                    obsidian_robot_count = state.obsidian_robot;
                }
                if (state.obsidian_robot < obsidian_robot_count - 1) {
                    continue;
                }
            }

            /* No point in building clay or obsidian robots in the last 2 minutes */
            if ((minute >= time - 2 && state.clay_robot < 1)
                || (minute >= time - 1 && state.obsidian_robot < 1)) {
                continue;
            }

            /* Unsafe optimization: Build a geode robot whenever you can */
            if (state.ore >= bp.geode_ore && state.obsidian >= bp.geode_obsidian) {
                add_state(NewRobot::GEODE, state, bp, new_states);
                continue;
            }
            if (minute < time - 1) {
                /* Unsafe optimization: build an obsidian robot whenever you can */
                if (state.ore >= bp.obsidian_ore && state.clay >= bp.obsidian_clay && state.obsidian_robot < obsidian_robot_limit) {
                    add_state(NewRobot::OBSIDIAN, state, bp, new_states);
                    continue;
                }
                /* Don't build clay and ore robots in the last few minutes. Plus
                 * unsafe optimization: Don't build more of these robots when there
                 * are already N (constants above). */
                if (minute < time - 2) {
                    if (state.ore >= bp.clay_ore && state.clay_robot < clay_robot_limit) {
                        add_state(NewRobot::CLAY, state, bp, new_states);
                    }
                    if (minute < time - 3) {
                        if (state.ore >= bp.ore_ore && state.ore_robot < ore_robot_limit) {
                            add_state(NewRobot::ORE, state, bp, new_states);
                        }
                    }
                }
            }
            add_state(NewRobot::NONE, state, bp, new_states);
        }
        current_states.swap(new_states);
    }
    int best_geode = 0;
    for (auto const& state : current_states) {
        if (state.geode > best_geode) {
            best_geode = state.geode;
        }
    }
    return best_geode;
}


int main()
{
    auto input = std::ifstream{"input19.txt", std::ios::in};
    if (!input.is_open()) {
        std::cerr << "failed to open input file" << std::endl;
        return 1;
    }

    std::vector<Blueprint> testBlueprints = {
        {4, 2, 3, 14, 2, 7},
        {2, 3, 3, 8, 3, 12},
    };
    std::cout << testBlueprints.size() << " test blueprints" << std::endl;

    auto const blueprints = readBlueprints(input);
    std::cout << blueprints.size() << " blueprints" << std::endl;

    // part 1 test
    std::cout << "-- part 1 test --" << std::endl;
    for (int index = 0; index < testBlueprints.size(); ++index) {
        std::cout << "Blueprint " << (index + 1)
                  << ": " << geodesFromBlueprint(testBlueprints[index], 24) << " geodes" << std::endl;
    }

    std::cout << "-- part 1 real input --" << std::endl;
    int part1 = 0;
    for (int index = 0; index < blueprints.size(); ++index) {
        int const geodes = geodesFromBlueprint(blueprints[index], 24);
        part1 += (index + 1) * geodes;
        std::cout << "Blueprint " << (index + 1) << ": " << geodes << " geodes" << std::endl;
    }
    std::cout << "Part 1 total: " << part1 << std::endl;

    // part 2 test
    std::cout << "-- part 2 test --" << std::endl;
    for (int index = 0; index < testBlueprints.size(); ++index) {
        std::cout << "Blueprint " << (index + 1)
                  << ": " << geodesFromBlueprint(testBlueprints[index], 32) << " geodes" << std::endl;
    }

    // part 2 real
    std::cout << "-- part 2 real input --" << std::endl;
    int part2 = 1;
    for (int index = 0; index < 3; ++index) {
        int const geodes = geodesFromBlueprint(blueprints[index], 32);
        part2 *= geodes;
        std::cout << "Blueprint " << (index + 1) << ": " << geodes << " geodes" << std::endl;
    }

    std::cout << "Part 2 total: " << part2 << std::endl;

    return 0;
}
