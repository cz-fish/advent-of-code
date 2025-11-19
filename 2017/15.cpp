#include <iostream>

constexpr unsigned int modulus = 2147483647;
constexpr unsigned int factorA = 16807;
constexpr unsigned int factorB = 48271;
constexpr unsigned int judge_bits = 0xffff;

/*
unsigned int mulmod_mersenne(
    unsigned long a,
    unsigned int b,
    unsigned int bits,
    unsigned int modulus) {

    const auto v = a * b;
    const auto s = (v & modulus) + (v >> bits);
    return s == modulus ? s - 1 : s;
}
*/

unsigned int mulmod_mersenne(
    unsigned long a,
    unsigned int b,
    unsigned int bits,
    unsigned int modulus) {

    return (a * b) % modulus;
}

unsigned int mulmod_mersenne_even(
    unsigned long a,
    unsigned int b,
    unsigned int bits,
    unsigned int modulus,
    unsigned int low_mask) {

    do {
        a = (a * b) % modulus;
        //std::cout << "v " << v << " lowmask " << low_mask << " and " << (v & low_mask) << std::endl;
        //break;
    } while (a & low_mask);
    return a;
}

int main(int, char**)
{
    unsigned int a = 65;
    unsigned int b = 8921;
    unsigned count = 0;
/*    for (unsigned i = 0; i < 40'000'000; ++i) {
        a = mulmod_mersenne(a, factorA, 31, modulus);
        b = mulmod_mersenne(b, factorB, 31, modulus);
        if ((a & judge_bits) == (b & judge_bits)) {
            ++count;
        }
    } */
    for (unsigned i = 0; i < 5'000'000; ++i) {
        a = mulmod_mersenne_even(a, factorA, 31, modulus, 3);
        //std::cout << "a " << a << std::endl;
        b = mulmod_mersenne_even(b, factorB, 31, modulus, 7);
        //std::cout << "b " << b << std::endl;
        if ((a & judge_bits) == (b & judge_bits)) {
            ++count;
        }
    }
    std::cout << count << std::endl;
}
