from collections import defaultdict
import re

import networkx as nx

with open("./input.txt") as f:
    ingredients = [re.match(r"^((?:\w+ ?)+)\(contains ((?:\w+(?:, )?)+)\)$", line).groups() for line in f.read().strip().splitlines()]
    ingredients = [(i[0].strip().split(" "), i[1].strip().split(", ")) for i in ingredients]

matches = defaultdict(lambda:[])

for ing, al in ingredients:
    for a in al:
        matches[a].append(set(ing))

G = nx.Graph()
for a, ma in matches.items():
    for m in set.intersection(*ma):
        G.add_edge(a, m)

allergens = {a: i for a, i in nx.bipartite.maximum_matching(G).items() if a in matches}

print("Answer 1:", len([i for ing in ingredients for i in ing[0] if i not in allergens.values()]))

al = sorted([(a, i) for a, i in allergens.items()], key=lambda i:i[0])
print("Answer 2:", ",".join([a[1] for a in al]))
