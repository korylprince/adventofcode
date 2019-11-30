import networkx as nx

points = []
with open("./input.txt") as f:
    for line in [line.strip() for line in f.read().strip().splitlines()]:
        points.append(tuple([int(n) for n in line.split(",")]))


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])


graph = nx.Graph()

for p1 in points:
    for p2 in points:
        if distance(p1, p2) <= 3:
            graph.add_edge(p1, p2)

graphs = nx.connected_component_subgraphs(graph)

print("Answer 1:", len(list(graphs)))
