import re

import networkx as nx

with open("./input.txt") as f:
    programs = [tuple(int(n) for n in re.findall(r"\d+", line)) for line in f.read().strip().splitlines()]

G = nx.Graph()
for p in programs:
    for p2 in p[1:]:
        G.add_edge(p[0], p2)

print("Answer 1:", len(nx.node_connected_component(G, 0)))
print("Answer 2:", len(list(nx.connected_components(G))))
