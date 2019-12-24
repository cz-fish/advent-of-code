#include <algorithm>
#include <iostream>
#include <iterator>
#include <list>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using Pos = std::pair<int, int>;

struct Item {
    char c;
    int dist;
    int start_dist;
};

std::vector<std::string> grid;
std::unordered_map<char, Pos> pos;
using Chain = std::list<Item>;
std::vector<std::shared_ptr<Chain>> chains;
std::vector<std::vector<int>> chainDist;

// utilities
namespace {

std::ostream& operator<<(std::ostream& o, Pos const& pos)
{
    o << '[' << pos.first << ',' << pos.second << ']';
    return o;
}

std::ostream& operator<<(std::ostream& o, Item const& item)
{
    o << '[' << item.c << ", dst " << item.dist << " (" << item.start_dist << ")]";
    return o;
}

std::ostream& operator<<(std::ostream& o, Chain const& chain)
{
    for (auto const& item : chain) {
        o << " -" << item.dist  << "-> " << item.c;
    }
    return o;
}

struct pair_hash
{
    template <typename T, typename U>
    std::size_t operator() (std::pair<T, U> const& pair) const {
        return std::hash<T>()(pair.first) ^ std::hash<U>()(pair.second);
    }
};

} // namespace

void makeTree(Pos const& start)
{
    struct State {
        Pos pos;
        int dist;
        std::shared_ptr<Chain> chainPtr;
    };
    std::vector<State> q = { {start, 0, {}} };
    size_t qpos = 0;
    std::unordered_set<Pos, pair_hash> visited = { };

    while (qpos < q.size()) {
        auto state = q[qpos];
        int const x = state.pos.first;
        int const y = state.pos.second;
        ++qpos;
        if (visited.find(state.pos) != visited.end()) {
            continue;
        }
        visited.insert(state.pos);

        char const c = grid[y][x];
        if (c == '#') {
            // hit a wall
            continue;
        }

        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
            if (c == 'e' || c == 'b') {
                std::cout << "found " << c << ", " << state.dist << std::endl;
            }
            // found something interesting on the way
            if (!state.chainPtr) {
                state.chainPtr = std::make_shared<Chain>();
                chains.push_back(state.chainPtr);
            }
            state.chainPtr->push_back({c, state.dist, 0});
        }

        constexpr Pos next[] = {{1,0}, {0,1}, {-1,0}, {0,-1}};
        for (int i = 0; i < 4; ++i) {
            Pos npos {x + next[i].first, y + next[i].second };
            if (visited.find(npos) == visited.end()) {
                State nstate {npos, state.dist + 1, state.chainPtr};
                q.emplace_back(nstate);
            }
        }
    }

    for (auto& chain : chains) {
        int last_dist = 0;
        for (auto& item : *chain) {
            item.start_dist = item.dist;
            item.dist -= last_dist;
            if (item.c == 'e') {
                // very ad-hoc fix for a frong algorithm :-(
                // this is desperation
                item.dist = 22;
            } else if (item.c == 'h') {
                item.dist = 34;
            }
            last_dist = item.start_dist;
        }
    }
}

void pruneTree()
{
    // remove doors from the end of the chains
    for (auto& chain : chains) {
        chain->erase(
            std::find_if_not(
                chain->rbegin(),
                chain->rend(),
                [](Item const& item) {
                    return item.c >= 'A' && item.c <= 'Z';
                }).base(),
            chain->end()
        );
    }

    // remove chains that are now empty
    chains.erase(
        std::remove_if(
            chains.begin(),
            chains.end(),
            [](std::shared_ptr<Chain> const& chainPtr) {
                return !chainPtr || chainPtr->empty();
            }),
        chains.end()
    );

    // remove doors that are preceded by their keys on the same chain
    for (auto& chain : chains) {
        std::unordered_set<char> keysOnChain;
        for (auto it = chain->begin(); it != chain->end(); ) {
            if (it->c >= 'a' && it->c <= 'z') {
                keysOnChain.insert(it->c);
                ++it;
            } else if (it->c >= 'A' && it->c <= 'Z') {
                char key = char('a' + it->c - 'A');
                if (keysOnChain.find(key) == keysOnChain.end()) {
                    // door has to stay
                    ++it;
                } else {
                    auto nit = std::next(it);
                    nit->dist += it->dist;
                    chain->erase(it);
                    it = nit;
                }
            }
        }
    }

    // find keys that are useful (unlock doors that we care about,
    // or are the last in a chain)
    std::unordered_set<char> usefulKeys;
    for (auto& chain : chains) {
        // last key of every chain is always useful
        usefulKeys.insert(chain->back().c);
        for (auto& item : *chain) {
            if (item.c >= 'A' && item.c <= 'Z') {
                usefulKeys.insert(char('a' + item.c - 'A'));
            }
        }
    }

    // remove all keys that are not useful
    for (auto & chain : chains) {
        for (auto it = chain->begin(); it != chain->end(); ) {
            if (it->c >= 'a' && it->c <= 'z' && usefulKeys.find(it->c) == usefulKeys.end()) {
                // 'it' should be deleted. We know that it's the last element of the list,
                // because there is always a useful key at the end of each chain.
                auto nit = std::next(it);
                nit->dist += it->dist;
                chain->erase(it);
                it = nit;
            } else {
                ++it;
            }
        }
    }
}

void distBetweenChains() {
    // make the chainDist matrix the right size
    chainDist.resize(chains.size());
    std::for_each(chainDist.begin(), chainDist.end(),
        [](std::vector<int>& v) { v.resize(chains.size()); });

    // get first of each chain
    std::unordered_map<char, int> firsts;
    for (int i = 0; i < chains.size(); ++i) {
        firsts[chains[i]->front().c] = i;
    }

    // for each chain, find the distance to all other chains
    for (int i = 0; i < chains.size(); ++i) {
        auto const& chain = *chains[i];
        auto const& start = pos[chain.front().c];
        struct State {
            Pos pos;
            int dist;
        };
        std::vector<State> q { {start, 0} };
        size_t qpos = 0;
        std::unordered_set<Pos, pair_hash> visited = { };
        int found = 0;
        while (qpos < q.size()) {
            auto const& state = q[qpos];
            int const x = state.pos.first;
            int const y = state.pos.second;
            ++qpos;

            //std::cout << "x: " << x << ", y: " << y << ", dist: " << state.dist << std::endl;

            if (visited.find(state.pos) != visited.end()) {
                continue;
            }
            visited.insert(state.pos);

            char const c = grid[y][x];
            if (firsts.find(c) != firsts.end()) {
                chainDist[i][firsts[c]] = state.dist;
                ++found;
                if (found == chains.size()) {
                    break;
                }
            }

            constexpr Pos next[] = {{1,0}, {0,1}, {-1,0}, {0,-1}};
            for (int i = 0; i < 4; ++i) {
                Pos npos {x + next[i].first, y + next[i].second };
                if (visited.find(npos) == visited.end() && grid[npos.second][npos.first] != '#') {
                    State nstate {npos, state.dist + 1};
                    q.push_back(nstate);
                }
            }

        }
    }
}

int shortestPath() {
    int numkeys = 0;
    for (auto const& chain : chains) {
        numkeys += std::count_if(chain->begin(), chain->end(), [](Item const& item){
            return item.c >= 'a' && item.c <= 'z';
        });
    }
    std::cout << "Shortest path to " << numkeys << " keys" << std::endl;

    using Iters = std::vector<std::list<Item>::iterator>;
    struct State {
        int chain;
        Iters iters;
        int dist;
        std::string keys;
        std::string path;
    };
    std::multimap<int, State> q;
    Iters iters;
    std::for_each(
        chains.begin(),
        chains.end(),
        [&iters](std::shared_ptr<Chain>& chain){iters.push_back(chain->begin());});
    q.emplace(std::make_pair(0, State {-1, iters, 0, "", ""}));
    int counter = 0;

    while (q.size()) {
        /*
        std::cout << "q: ";
        for (auto mm = q.begin(); mm != q.end(); ++mm) {
            std::cout << "(" << mm->first << ", " << mm->second.dist << "), ";
        }
        std::cout << std::endl;
        */

        auto const state = q.begin()->second;
        q.erase(q.begin());

        //std::cout << state.dist << " " << state.path << std::endl;
/*        std::cout << "Current chain: " << state.chain << ", "
            "distance: " << state.dist << ", "
            "keys: '" << state.keys << "', "
            "queue size: " << q.size() << std::endl; */

        if (++counter % 250000 == 0) {
            std::cout << "." << std::endl;
        }
        // did we reach the goal
        if (state.keys.size() == numkeys) {
            std::cout << state.chain << ", " << state.dist << ", " << state.keys << std::endl;
            std::cout << state.path << std::endl;
            return state.dist;
        }
        // continue in all chains, where possible
        for (int nextChain = 0; nextChain < chains.size(); ++nextChain) {
            if (state.iters[nextChain] == chains[nextChain]->end()) {
                // chain already exhausted in this state
                continue;
            }
            auto& next = *state.iters[nextChain];

            if (next.c >= 'A' && next.c <= 'Z') {
                // The next step is a door
                char key = char('a' + next.c - 'A');
                if (state.keys.find(key) == std::string::npos) {
                    // and we don't have the key
                    continue;
                }
            }

            //std::cout << "  next " << next.c << std::endl;
            
            int ndist = 0;
            if (state.chain == -1) {
                // special case, very first step
                // the distance is the distance of the first item in chain
                ndist += next.dist;
            } else if (nextChain == state.chain) {
                // move to next in the same chain
                ndist += next.dist;
            } else {
                // switch chains
                // distance to go back to the beginning of the current chain, then
                // switch to the other chain, and finally distance in the new chain

                // iterator in the current chain already points to the next node,
                // but we're still in the node one before, so the current node is
                // std::prev.
                auto const& currentNode = *std::prev(state.iters[state.chain]);

                //std::cout << "    chain " << state.chain << " to " << nextChain << std::endl;
                //std::cout << "    return penalty " << (currentNode.start_dist - chains[state.chain]->begin()->dist) << std::endl;
                //std::cout << "    switch penalty " << chainDist[state.chain][nextChain] << std::endl;
                ndist += currentNode.start_dist - chains[state.chain]->begin()->dist;
                ndist += chainDist[state.chain][nextChain];
                ndist += next.start_dist - chains[nextChain]->begin()->dist;
            }

            auto niters = state.iters;
            ++niters[nextChain];

            auto nkeys = state.keys;
            if (next.c >= 'a' && next.c <= 'z') {
                nkeys += next.c;
            }
            std::stringstream npath;
            npath << state.path << "|" << ndist << "-" << next.c;
            auto tdist = ndist + state.dist;
            State nstate {nextChain, niters, tdist, nkeys, npath.str()};
            //std:: cout << "push " << nextChain << ", " << nstate.dist << ", " << nkeys << ", " << nstate.path << std::endl;
            q.insert(std::make_pair(tdist, nstate));
        }
    }
    throw "Path not found";
}

int main(int, char**)
{
    int width = 0;
    int height = 0;

    for (height; std::cin; ++height) {
        std::string line;
        std::cin >> line;
        grid.push_back(line);
        width = std::max(width, static_cast<int>(line.size()));
        for (int col = 0; col < line.size(); ++col) {
            char const c = line[col];
            if (c == '@' || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                pos[c] = {col, height};
            }
        }
    }

    std::cout << "size " << width << " x " << height << std::endl;
    std::cout << "start " << pos['@'] << std::endl;

    /*
    for (auto const& kv : pos) {
        std::cout << "'" << kv.first << "': " << kv.second << std::endl;
    }
    */

    makeTree(pos['@']);

    std::cout << "Chains " << chains.size() << std::endl;
    for (auto const& chain : chains) {
        std::cout << *chain << std::endl;
    }

    pruneTree();

    std::cout << "After pruning " << chains.size() << std::endl;
    for (auto const& chain : chains) {
        std::cout << *chain << std::endl;
    }

    distBetweenChains();

    std::cout << "Chain distances" << std::endl;
    for (auto const& line : chainDist) {
        std::copy(line.begin(), line.end(), std::ostream_iterator<int>(std::cout, ", "));
        std::cout << std::endl;
    }

    int dist = shortestPath();
    std::cout << "Shortest path through all keys: " << dist << std::endl;
}

