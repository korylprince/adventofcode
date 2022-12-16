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

def dfs(target, pres, minute, off, node):
    max = pres
    for v, r, l in [(v, r, shortpathlen[node][v] + 1) for v, r in worthit.items() if v in off]:
        if minute + l > target:
            continue
        off.remove(v)
        next = dfs(target, pres + (target-minute-l)*r, minute + l, off, v)
        if next > max:
            max = next
        off.add(v)
    return max

part1 = dfs(30, 0, 0, set(worthit.keys()), "AA")
print("Answer 1:", part1)

bitfield = {v: 2**idx for idx, v in enumerate(worthit.keys())}

def tobitfield(path):
    return sum(bitfield[p] for p in path)

def dfspaths(target, pres, minute, off, node, path):
    paths = [(pres, tobitfield(path))]
    for v, r, l in [(v, r, shortpathlen[node][v] + 1) for v, r in worthit.items() if v in off]:
        if minute + l > target:
            continue
        off.remove(v)
        paths += dfspaths(target, pres + (target-minute-l)*r, minute + l, off, v, path + (v,))
        off.add(v)
    return paths

allpaths = sorted(dfspaths(26, 0, 0, set(worthit.keys()), "AA", tuple()), reverse=True)
allpaths = [p for p in allpaths if p[0] > part1//2]
cross = [s1+s2 for (s1, p1), (s2, p2) in combinations(allpaths, 2) if p1&p2 == 0]
print("Answer 2:", max(cross))
