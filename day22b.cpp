#include <set>
#include <iostream>
#include <unordered_map>

/*int const depth = 5913;
int const tx = 8;
int const ty = 701;
*/

int const depth = 510;
int const tx = 10;
int const ty = 10;


int constexpr maxx = 1000;
int constexpr maxy = 1000;
int levels[maxy][maxx];
int types[maxy][maxx];

// rocky = 0
// wet = 1
// narrow = 2
int const empty = 0;
int const torch = 1;
int const climb = 2;

int const top = 0;
int const left = 1;
int const right = 2;
int const down = 3;

int set_types_get_risk() {
    int risk = 0;
    for (int y = 0; y < maxy; ++y) {
        for (int x = 0; x < maxx; ++x) {
            int index;
            if (x == 0 && y == 0) {
                index = 0;
            } else if (x == tx && y == ty) {
                index = 0;
            } else if (y == 0) {
                index = 16807 * x;
            } else if (x == 0) {
                index = 48271 * y;
            } else {
                index = levels[y][x-1] * levels[y-1][x];
            }
            int el = (index + depth) % 20183;
            levels[y][x] = el;
            int r = el % 3;
            if (x <= tx && y <= ty) {
                risk += r;
            }
            types[y][x] = r;
        }
    }
    return risk;
}

struct State {
    int time;
    int x;
    int y;
    int item;
    int from;

    State(int time, int x, int y, int item, int from):
        time(time), x(x), y(y), item(item), from(from) {}
    bool operator<(State const& other) const {
        return time < other.time;
    }
};

std::ostream& operator<< (std::ostream& os, State const& st) {
    return os << "[" << st.time << ", " << st.x << ", " << st.y << ", " << st.item << "]";
}

using BestsMap = std::unordered_map<long, int>;

void step(int nx, int ny, int from, int otime, int oitem, std::multiset<State> &prog, BestsMap &bests)
{
    if (nx < 0 || ny < 0 || nx >= 15 /*maxx*/ || ny >= maxy) {
        return;
    }

    int type = types[ny][nx];
    int ntime = (type == oitem)? otime + 8: otime + 1;

    long coords = (ny * maxx) + nx;
    auto f = bests.find(coords);
    if (f != bests.end() && f->second /* +7 ?? */ <= ntime) {
        return;
    }

    bests[coords] = ntime;

    if (type == oitem) {
        // item not wearable in this env.
        prog.emplace(ntime, nx, ny, (oitem + 1)%3, from);
        prog.emplace(ntime, nx, ny, (oitem + 2)%3, from);
    } else {
        prog.emplace(ntime, nx, ny, oitem, from);
    }
}

int walk() {
    std::multiset<State> prog;
    prog.emplace(0, 0, 0, torch, top);

    BestsMap bests;
    bests[0] = 0;

    int best = -1;
    int counter = 0;

    while(true) {
        ++counter;

        auto f = prog.begin();
        auto st = *f;
        prog.erase(f);

        if (best != -1 && st.time >= best + 7) {
            return best + 7;
        }

        if (st.x == tx && st.y == ty) {
            if (st.item == torch) {
                return st.time;
            }
            if (best == -1) {
                best = st.time;
            }
        }

//        std::cout << counter << ", " << best << ", " << st << ", " << prog.size() << std::endl;
        if (counter == /*50*/ 100000) {
            std::cout << counter << ", " << best << ", " << st << ", " << prog.size() << std::endl;
//            return 0;
            counter = 0;
        }

        if (st.from != down) {
            step(st.x, st.y+1, top, st.time, st.item, prog, bests);
        }
        if (st.from != left) {
            step(st.x-1, st.y, right, st.time, st.item, prog, bests);
        }
        if (st.from != top) {
            step(st.x, st.y-1, down, st.time, st.item, prog, bests);
        }
        if (st.from != right) {
            step(st.x+1, st.y, left, st.time, st.item, prog, bests);
        }
    }
}

int main(int, char**)
{
    std::cout << "Risk " << set_types_get_risk() << std::endl;

    std::cout << "Shortest " << walk() << std::endl;

    return 0;
}