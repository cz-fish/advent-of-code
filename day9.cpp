#include <iostream>
#include <memory>
#include <utility>
#include <vector>

struct ll {
    using ptr = std::shared_ptr<ll>;
    ptr prev, next;
    int val;

    ll(int val): val(val) {}
    ll(int val, ptr prev, ptr next): val(val), prev(prev), next(next) {}
};

uint64_t play(int players, int marbles)
{
    std::shared_ptr<ll> current = std::make_shared<ll>(0);
    current->prev = current;
    current->next = current;

    uint64_t max_score = 0;
    int player = 0;

    std::vector<uint64_t> scores(players);

    for (int i = 1; i <= marbles; ++i) {
        if (i % 23 == 0) {
            for (int j = 0; j < 7; ++j) {
                current = current->prev;
            }
            scores[player] += i + current->val;
            if (scores[player] > max_score) max_score = scores[player];
            current->prev->next = current->next;
            current->next->prev = current->prev;
            current = current->next;
        }
        else {
            current = current->next;
            auto ins = std::make_shared<ll>(i, current, current->next);
            current->next->prev = ins;
            current->next = ins;
            current = ins;
        }

        player = (player + 1) % players;
    }

    return max_score;
}

int main(int argc, char** argv)
{
    if (argc < 3) {
        std::cerr << "Missing parameters" << std::endl;
        return 1;
    }

    int players = std::atoi(argv[1]);
    int marbles = std::atoi(argv[2]);

    std::cout << "players " << players << ", marbles " << marbles << std::endl;

    uint64_t score = play(players, marbles);

    std::cout << "score " << score << std::endl;

    return 0;
}
