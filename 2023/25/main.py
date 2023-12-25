import re
import networkx as nx
import math

G = nx.Graph()
with open("./input.txt") as f:
    lines = [re.findall("[a-z]+", line) for line in f.read().strip().splitlines()]
    components = {line[0]:set(line[1:]) for line in lines}
    for c, other in components.items():
        for c2 in other:
            G.add_edge(c, c2)

# feels a bit like cheating, but here we are...
G.remove_edges_from(nx.minimum_edge_cut(G))

print("Answer 1:", math.prod(len(c) for c in nx.connected_components(G)))
