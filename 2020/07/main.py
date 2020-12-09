import re
from collections import deque

import networkx as nx

ruleRegexp = r"^(\w+ \w+) bags contain ((?:\d+ \w+ \w+ bags?(?:, )?)+|no other bags)\.$"
subRuleRegexp = r"^(\d+) (\w+ \w+) bags?$"

G = nx.DiGraph()

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        n, subs = re.match(ruleRegexp, line).groups()
        if n not in G:
            G.add_node(n)
        if subs == "no other bags":
            continue
        for k, sn in [re.match(subRuleRegexp, s).groups() for s in subs.split(", ")]:
            G.add_edge(n, sn, weight=int(k))

print("Answer 1:", len({edge[0] for edge in nx.edge_dfs(G, "shiny gold", orientation="reverse")}))

def bfs(G, root):
    q = deque((([root], 1),))
    count = -1
    while len(q) > 0:
        path, multiplier = q.popleft()
        n = path[-1]
        count += multiplier
        for sn in G.successors(n):
            weight = G.get_edge_data(n, sn)["weight"]
            q.append((path + [sn], multiplier * weight))

    return count

print("Answer 2:", bfs(G, "shiny gold"))
