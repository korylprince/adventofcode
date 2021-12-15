import heapq

G = dict()

with open("./input.txt") as f:
    for y, row in enumerate(f.read().strip().splitlines()):
        for x, v in enumerate(row):
            G[(x, y)] = int(v)

START = (0, 0)
END = (max([x for x, y in G.keys()]), max([y for x, y in G.keys()]))
rows, cols = END[1] + 1, END[0] + 1
d = ((0, 1), (0, -1), (1, 0), (-1, 0))

def dijkstra(G, end):
    seen = set((START,))
    h = [(0, START)]
    while len(h) > 0:
        cost, p = heapq.heappop(h)
        if p == end:
            return cost
        for dx, dy in d:
            p1 = (p[0]+dx, p[1]+dy)
            if p1 in seen or p1 not in G:
                continue
            seen.add(p1)
            heapq.heappush(h, (cost + G[p1], p1))

print("Answer 1:", dijkstra(G, END))

for x in range(cols*5):
    for y in range(rows*5):
        if (x, y) in G:
            continue
        v = G[(x%cols, y%rows)] + x//cols + y//rows
        G[(x, y)] = (v - 1) % 9 + 1

END = (rows*5-1, cols*5-1)
print("Answer 2:", dijkstra(G, END))
