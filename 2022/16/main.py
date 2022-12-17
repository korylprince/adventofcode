import re
import math
from itertools import combinations

import networkx as nx

G = nx.Graph()

with open("./input.txt") as f:
    lines = [re.findall(r"([A-Z]{2}).*=(\d+);.*?((?:[A-Z]{2}(?:, )?)+)", line)[0] for line in f.read().strip().splitlines()]
    lines = [(v, int(r), edges.split(", ")) for v, r, edges in lines]
    valves = {v: (r, edges) for v, r, edges in lines}
    worthit = {v: r for v, (r, _) in valves.items() if r > 0}

for v, r, edges in lines:
    for v2 in edges:
        G.add_edge(v, v2)

shortpathlen = {v: lens for v, lens in nx.all_pairs_shortest_path_length(G)}
bitfield = {v: 2**idx for idx, v in enumerate(list(worthit.keys()) + ["AA"])}
shortpath = {b1|b2: shortpathlen[v1][v2] for v1, b1 in bitfield.items() for v2, b2 in bitfield.items() if v1 != v2}
worth = {bitfield[v]: r for v, r in worthit.items()}


def dfs(target, pres, minute, on, node):
    max = pres
    for v, r, l in [(v, r, shortpath[node | v] + 1) for v, r in worth.items() if v & on == 0]:
        if minute + l > target:
            continue
        if (next := dfs(target, pres + (target-minute-l)*r, minute + l, on | v, v)) > max:
            max = next
    return max

part1 = dfs(30, 0, 0, 0, bitfield["AA"])
print("Answer 1:", part1)


def dfspaths(target, pres, minute, on, node, path):
    paths = [(pres, path)]
    for v, r, l in [(v, r, shortpath[node | v] + 1) for v, r in worth.items() if v & on == 0]:
        if minute + l > target:
            continue
        paths += dfspaths(target, pres + (target-minute-l)*r, minute + l, on | v, v, path | v)
    return paths

allpaths = sorted(dfspaths(26, 0, 0, 0, bitfield["AA"], 0), reverse=True)
allpaths = [p for p in allpaths if p[0] > part1//2]
cross = [s1+s2 for (s1, p1), (s2, p2) in combinations(allpaths, 2) if p1&p2 == 0]
print("Answer 2:", max(cross))
