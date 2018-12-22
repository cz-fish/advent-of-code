#include <set>
#include <iostream>
#include <unordered_map>


int const depth = 5913;
int const tx = 8;
int const ty = 701;


/*
int const depth = 510;
int const tx = 10;
int const ty = 10;
*/


int constexpr maxx = 2000;
int constexpr maxy = 2000;
int levels[maxy][maxx];
int types[maxy][maxx];

// rocky = 0
// wet = 1
// narrow = 2
int const empty = 0;
int const torch = 1;
int const climb = 2;

int shortest[3][maxy][maxx];

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

int go()
{
    int xlimit = 100;
    int ylimit = 720;

    for (int y = 0; y < maxy; ++y) {
        for (int x = 0; x < maxx; ++x) {
            for (int i = 0; i < 3; ++i) {
                shortest[i][y][x] = 9999;
            }
        }
    }

    shortest[torch][0][0] = 0;

    for (int repeat = 0; repeat < 2000; ++repeat) {

    for (int y = 0; y < ylimit; ++y) {
        for (int x = 0; x < xlimit; ++x) {
            int type = types[y][x];
            int ttype = y > 0? types[y-1][x]: 0;
            int ltype = x > 0? types[y][x-1]: 0;

            for (int i = 1; i <= 2; ++i) {
                int t = (type + i) % 3;

                int M = shortest[t][y][x];
                int m = M;
                if (y > 0 && t != ttype) {
                    for (int j = 0; j < 3; j++) {
                        if (j == ttype) { continue; }
                        int b = shortest[j][y-1][x] + 1;
                        if (j != t) { b += 7; }
                        if (b < m) { m = b; }
                    }
                }

                if (x > 0 && t != ltype) {
                    for (int j = 0; j < 3; j++) {
                        if (j == ltype) { continue; }
                        int b = shortest[j][y][x-1] + 1;
                        if (j != t) { b += 7; }
                        if (b < m) { m = b; }
                    }
                }

                if (m < M) {
                    shortest[t][y][x] = m;
                }
            }
        }
    }

    for (int y = ylimit - 1; y >=0; --y) {
        for (int x = xlimit - 1; x >= 0; --x) {
            int type = types[y][x];
            int btype = types[y+1][x];
            int rtype = types[y][x+1];

            for (int i = 1; i <= 2; ++i) {
                int t = (type + i) % 3;

                int M = shortest[t][y][x];
                int m = M;
                if (t != btype) {
                    for (int j = 0; j < 3; j++) {
                        if (j == btype) { continue; }
                        int b = shortest[j][y+1][x] + 1;
                        if (j != t) { b += 7; }
                        if (b < m) { m = b; }
                    }
                }

                if (t != rtype) {
                    for (int j = 0; j < 3; j++) {
                        if (j == rtype) { continue; }
                        int b = shortest[j][y][x+1] + 1;
                        if (j != t) { b += 7; }
                        if (b < m) { m = b; }
                    }
                }

                if (m < M) {
                    shortest[t][y][x] = m;
                }
            }
        }
    }
    }

    return shortest[torch][ty][tx];
}

int main(int, char**)
{
    std::cout << "Risk " << set_types_get_risk() << std::endl;

    std::cout << "Shortest " << go() << std::endl;

    return 0;
}