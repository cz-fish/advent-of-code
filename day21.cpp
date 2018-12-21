#include <iostream>
#include <unordered_map>
#include <unordered_set>

int main(int, char**)
{
    int counter = 0;
    std::unordered_map<unsigned int, unsigned int> s;
    std::unordered_set<unsigned int> v;

    unsigned int r2 = 0;
    unsigned int r3 = 0;
    unsigned int prev_r3 = 0;

    while (true) {
        r2 = r3 | 65536;
        r3 = 14070682;

        while (true) {
            r3 = (((r3 + (r2 & 255)) & 16777215) * 65899) & 16777215;
            if (r2 < 256) {
                ++counter;
                if (v.find(r3) != v.end()) {
                    std::cout << r3 << ", " << prev_r3 << ", " << counter << std::endl;
                    return 0;
                }
                v.insert(r3);
                prev_r3 = r3;
//                std::cout << r2 << ", " << r3 << std::endl;
/*                auto x = s.find(r2);
                if (x != s.end()) {
                    std::cout << r2 << ", " << r3 << ", " << x->second << std::endl;
                    return 0;
                } else {
                    s[r2] = r3;
                } */
/*                ++counter;
                if (counter > 1000) {
                    return 0;
                } */
                break;
            } else {
                r2 /= 256;
            }
        }
    }
}
