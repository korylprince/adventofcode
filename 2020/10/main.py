from collections import defaultdict

import networkx as nx

with open("./input.txt") as f:
    adapters = [int(line.strip()) for line in f.read().strip().splitlines()]

source = 0
sink = max(adapters) + 3
adapters += [source, sink]
adapters.sort()

weights = []

for u, v in nx.utils.pairwise(adapters):
    weights.append(v-u)

print("Answer 1:", weights.count(1) * weights.count(3))

counts = defaultdict(lambda:0)
counts[source] = 1

for u in adapters:
    for v in adapters:
        if 1 <= v - u <= 3:
            counts[v] += counts[u]

print("Answer 2:", counts[sink])
