from itertools import combinations

import networkx as nx

with open("./input.txt") as f:
    cubes = set([tuple(int(n) for n in line.strip().split(",")) for line in f.read().strip().splitlines()])

def find_area(cubes):
    area = 6 * len(cubes)

    for c1, c2 in combinations(cubes, 2):
        if abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]) == 1:
            area -= 2

    return area

area = find_area(cubes)
print("Answer 1:", area)

# graph air surrounding and in blob
maxx = max([x for x, y, z in cubes])
maxy = max([y for x, y, z in cubes])
maxz = max([z for x, y, z in cubes])

outside = (maxx, maxy, maxz+1)
empty = set((outside,))
G = nx.Graph()
G.add_node(outside)
for x in range(maxx+1):
    for y in range(maxy+1):
        for z in range(maxz+1):
            if (p := (x, y, z)) not in cubes:
                empty.add(p)
                G.add_node(p)


for c1, c2 in combinations(empty, 2):
    if abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]) == 1:
        G.add_edge(c1, c2)

# find distinct subgraphs
air = nx.connected_components(G)

for a in [a for a in air if outside not in a]:
    area -= find_area(a)

print("Answer 2:", area)
