#include <iostream>
#include <vector>


int van_eck(std::vector<int> const& start, int const K)
{
    auto memory = std::vector<int>(K);
    for (size_t i = 0; i < start.size(); ++i) {
        memory[start[i]] = i + 1;
    }

    int last_said = 0;
    int next = 0;
    int turn = start.size() + 1;

    while (turn <= K) {
        last_said = next;
        next = memory[last_said];
        if (next != 0) {
            next = turn - next;
        }
        memory[last_said] = turn;
        ++turn;
    }
    return last_said;
}

int main()
{
    std::cout << van_eck({13, 16, 0, 12, 15, 1}, 30000000) << std::endl;
    return 0;
}
