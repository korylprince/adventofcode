import numpy as np

with open("./input.txt") as f:
    lengths = [int(l.strip()) for l in f.read().strip().split(",")]

rope = np.array(range(256))
pos = 0
skip = 0

def rotate(arr, n):
    n = n % len(rope)
    arr = np.concatenate((arr[n:], arr[:n]))
    return arr

for l in lengths:
    rope[:l] = np.flip(rope[:l])
    pos += l + skip
    rope = rotate(rope, l + skip)
    skip += 1

rope = rotate(rope, len(rope) - (pos % len(rope)))

print("Answer 1:", rope[0] * rope[1])
