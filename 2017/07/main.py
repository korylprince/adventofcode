import re

import networkx as nx

nodeRegexp = "(?P<name>[a-z]+) \((?P<weight>\d+)\)( -> (?P<children>.*))?"

with open("./input.txt") as f:
    nodes = [re.match(nodeRegexp, line).groupdict() for line in f.read().strip().splitlines()]

graph = nx.DiGraph()

for node in nodes:
    graph.add_node(node["name"], weight=int(node["weight"]))

for node in nodes:
    if node["children"] is None:
        continue
    for child in [c.strip() for c in node["children"].strip().split(",")]:
        graph.add_edge(node["name"], child)

root = [n for n, d in graph.in_degree() if d==0][0]
print("Answer 1:", root)

errors = []

def weight(node):
    w = graph.node[node]["weight"]
    children = []
    for child in graph[node].keys():
        cw = weight(child)
        w += cw
        children.append(cw)

    if len(set(children)) > 1:
        errors.append({c: weight(c) for c in graph[node].keys()})

    return w

weight(root)
min_error = min([min(c.values()) for c in errors])
error = [c for c in errors if min(c.values()) == min_error][0]
diff = max(error.values()) - min(error.values())
bad_node = [k for k, v in error.items() if list(error.values()).count(v) == 1][0]
print("Answer 2:", graph.node[bad_node]["weight"] - diff)
