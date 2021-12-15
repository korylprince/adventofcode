from collections import defaultdict, Counter
from itertools import pairwise

with open("./input.txt") as f:
    polys, rules = f.read().strip().split("\n\n")
    # ABCD -> {AB: 1, BC: 1, CD: 1}
    pairs = defaultdict(lambda:0, Counter(["".join(p) for p in pairwise(polys)]))
    # ABCD -> {A: 1, B: 1, C: 1, D: 1}
    polymers = defaultdict(lambda:0, Counter(polys))
    rules = {pair: res for pair, res in [row.strip().split(" -> ") for row in rules.strip().splitlines()]}

def step(polymers, pairs, rules):
    new = defaultdict(lambda:0)
    for pair, res in rules.items():
        new[pair[0]+res] += pairs[pair]
        new[res+pair[1]] += pairs[pair]
        polymers[res] += pairs[pair]

    return new

for i in range(10):
    pairs = step(polymers, pairs, rules)

print("Answer 1:", max(polymers.values()) - min(polymers.values()))

for i in range(30):
    pairs = step(polymers, pairs, rules)

print("Answer 2:", max(polymers.values()) - min(polymers.values()))
