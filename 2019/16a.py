#!/usr/bin/python3.8


def fft(input):
    output = [0] * len(input)
    base = [0, 1, 0, -1]
    for i in range(len(input)):
        acc = input[i]
        basepos = 1
        repeats = 1
        for j in range(i+1, len(input)):
            if repeats == i + 1:
                repeats = 0
                basepos = (basepos + 1) % 4
            acc += input[j] * base[basepos]
            repeats += 1
        if acc < 0:
            acc = -acc
        output[i] = acc % 10
    return output


def fft_repeats(line, repeats):
    dig = [ord(c) - ord('0') for c in line]
    for i in range(repeats):
        dig = fft(dig)
    fftresult = ''.join([str(d) for d in dig[:8]])
    print(f'{line[:10]}... FFT = {fftresult}')


fft_repeats("12345678", 4)
fft_repeats("80871224585914546619083218645595", 100)
fft_repeats("19617804207202209144916044189917", 100)
fft_repeats("69317163492948606335995924319873", 100)
with open('input16.txt', 'rt') as f:
    line = f.readline().strip()
fft_repeats(line, 100)
