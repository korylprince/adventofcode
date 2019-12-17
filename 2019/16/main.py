import itertools

import numpy as np

with open("./input.txt") as f:
    data = np.array([int(d) for d in f.read().strip()])

def gen_pattern(length):
    return np.array(
        [np.array(list(itertools.islice(
            itertools.cycle([0] * size + [1] * size + [0] * size + [-1] * size),
            1, length + 1)))
        for size in range(1, length + 1)]
    )

def fft(data, pattern):
    return abs(np.matmul(data, pattern)) % 10

def ffts(data, pattern, count):
    for i in range(count):
        data = fft(data, pattern)

    return data

pattern = np.flipud(np.rot90(gen_pattern(len(data))))
print("Answer 1:", ("{}"*8).format(*ffts(data, pattern, 100)[:8]))

def fftcheat(data):
    for i in range(len(data) - 2, -1, -1):
        data[i] = (data[i] + data[i+1]) % 10

def fftscheat(data, count):
    for i in range(count):
        fftcheat(data)
    return data

with open("./input.txt") as f:
    text = f.read().strip() * 10_000
    offset = int(text[:7])
    data = np.array([int(d) for d in text])[offset:]

print("Answer 2:", ("{}"*8).format(*fftscheat(data, 100)[:8]))
