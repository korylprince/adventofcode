import re

with open("./input.txt") as f:
    sequences = [[int(n) for n in re.findall(r"-?\d+", line)] for line in f.read().strip().splitlines()]

def lagrange(sequence):
    def f(x, idx):
        num = 1
        den = 1
        for xn in [xn for xn in range(len(sequence)) if xn != idx]:
            num *= (x - xn)
            den *= (idx - xn)
        return int(num / den)

    def g(x):
        return sum(sequence[idx] * f(x, idx) for idx in range(len(sequence)))

    return g

lagranges = [lagrange(s) for s in sequences]
print("Answer 1:", sum([l(len(sequences[0])) for l in lagranges]))
print("Answer 2:", sum([l(-1) for l in lagranges]))
