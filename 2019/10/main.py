import math
import itertools

import networkx as nx

ast = set()

with open("./input.txt") as f:
    for y, row in enumerate([[d for d in row.strip()] for row in f.read().strip().splitlines()]):
        for x, d in enumerate(row):
            if d == "#":
                ast.add((x, y))

def slope(a, b):
    x, y = b[0] - a[0], b[1] - a[1]
    while (g := math.gcd(x, y)) > 1:
        x, y = x//g, y//g
    return x, y

def rad(x1, y1, x2, y2):
    o = math.atan2(x2 - x1, y1 - y2)
    if o < 0:
        return 2 * math.pi + o
    return o

def get_graph(ast):
    graph = nx.Graph()
    for a, b in itertools.combinations(ast, 2):
        if (a, b) in graph.edges:
            continue

        dx, dy = slope(a, b)
        x, y = a
        while True:
            x, y = x + dx, y + dy
            if (x, y) in ast:
                graph.add_edge(a, (x, y))
                break

    return graph

best, edges = max(dict(get_graph(ast).degree()).items(), key=lambda i: i[1])
print("Answer 1:", edges)

destroyed = 0

while destroyed < 200:
    graph = get_graph(ast)
    for a in sorted(graph.neighbors(best), key=lambda a: rad(best[0], best[1], a[0], a[1])):
        ast.remove(a)
        destroyed += 1
        if destroyed == 200:
            print("Answer 2:", a[0] * 100 + a[1])
            break
