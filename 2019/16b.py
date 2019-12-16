#!/usr/bin/python3.8

multiplier = 10000

"""
Explanation
-----------

We know how long is the input (10000 * length of input file = 6.5 million), and we know which 8
digits we are interested in (7 first digits of input is the offset).

Naive solution would take these 8 digits that we want to compute, and solve recursively - as a sum
of those positions that have 1 in the FFT pattern, minus sum of those that have -1 in the FFT pattern,
ignoring all those that have 0 in the FFT pattern. The recursion would be 100 levels deep. In every
level (from 100 down to 1), we could ignore 1/2 of the digits of the lower level. However, that still
means that we have have to compute 3.25 million values on every of the 100 levels of recursion. That
is not feasible.

(Useless) observation - on level 0, we repeat the input sequence 10000 times, and the base pattern for
the first element in 1 0 -1 0 (length 4). The least common multiple of 4 and 650 is 1300, so after every
2 repetitions of the input, the pluses and minuses will annihilate each other and the result for that digit
will be 0. That is true for every digit whose base pattern length has a common multiple with 650 (or
something of that sort). However, if anything, this would only be useful for calculating values on level 1,
and cannot be extended to later levels.

(Useful) observation - when we apply FFT on the input once, we can see that the first half are just random
number, but the second half of the output is periodical. The length of the period is proportional to the
length of the input (650) and the multiplier (10000). Why is the second half periodical?

(Useful) observation - the result value of i-th element of the array is not impacted by the values of
elements between 0 and i at all. That is because they all have weight 0 in the i-th iteration of the base
pattern, and i is the first 1 in the pattern.

input:       1  2  3  4  5  6  7  ...
i=0:     (0) 1  0 -1  0  1 -1  0  ...
i=1:     (0) 0  1  1  0  0 -1 -1  ...
i=2:     (0) 0  0  1  1  1  0  0  ...
i=3:     (0) 0  0  0  1  1  1  1  ...
i=4:     (0) 0  0  0  0  1  1  1  ...
i=5:     (0) 0  0  0  0  0  1  1  ...
i=6:     (0) 0  0  0  0  0  0  1  ...

(Useful) observation - when i is greater than 1/2 of the (input size * multiplier) - all elements before i
will have coefficient 0, and all elements from i to the end will have coefficient 1. That is because the
FFT pattern for the i-th element is (i-1) zeroes, followed by i ones, and we know that 2 * i >= input length.

(Final) observation - in all the examples, as well as in the problem input, the offset of the requested
digits is always in the second half of the array.

This means that all we need to do is to add all numbers from i-th position to the end, and repeat this
100 times. There is an opportunity for improvement, since the sums on each level will be periodical. On
the first level, we only need to compute 6500 last sums (650 is the size of input - sum of these 650 digits
modulo 10 is X, and 10*X modulo 10 has to be 0, hence the period on level 1 will be at most 6500 long).
Etc. on the higher levels.

However, since we only need to do ~ 500k * 100 additions anyway, the program finishes reasonably quickly
even without any optimizations.
"""


def fft_repeats(line, repeats):
    offset = int(line[:7])
    inlen = len(line)
    length = inlen * multiplier
    assert(offset > length // 2)
    dig = [ord(c) - ord('0') for c in line]

    work = [0] * (length - offset)
    p = inlen - 1
    for i in range(len(work)-1, -1, -1):
        work[i] = dig[p]
        p = (p-1) % inlen
    
    for step in range(repeats):
        s = 0
        for i in range(len(work)-1, -1, -1):
            s = (s + work[i]) % 10
            work[i] = s
    
    print(''.join([str(d) for d in work[:8]]))
    return


fft_repeats("03036732577212944063491565474664", 100)
#fft_repeats("02935109699940807407585447034323", 100)
#fft_repeats("03081770884921959731165446850517", 100)

with open('input16.txt', 'rt') as f:
    line = f.readline().strip()
fft_repeats(line, 100)
