from itertools import pairwise
import networkx as nx

G = nx.DiGraph()

with open("./input.txt") as f:
    first, second = f.read().strip().split("\n\n")
    order = [[int(n) for n in line.strip().split("|")] for line in first.strip().splitlines()]
    updates = [[int(n) for n in line.strip().split(",")] for line in second.strip().splitlines()] 

for a, b in order:
    G.add_edge(a, b)

def check_update(update):
    for a, b in pairwise(update):
        if not G.has_edge(a, b):
            return False
    return True

print("Answer 1:", sum([u[len(u) // 2] for u in updates if check_update(u)]))

fixed = [nx.dag_longest_path(G.subgraph(u)) for u in updates if not check_update(u)]
print("Answer 2:", sum([u[len(u) // 2] for u in fixed]))
