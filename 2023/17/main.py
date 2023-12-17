import heapq

G = dict()
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, digit in enumerate(line.strip()):
            G[(x, y)] = int(digit)

def dijkstra(start, target, min, max):
    seen = set()
    # heat, (x, y), (dx, dy), length
    q = [(0, start, (1, 0), 1), (0, start, (0, 1), 1)]
    heapq.heapify(q)
    while len(q) > 0:
        heat, (x, y), (dx, dy), length = heapq.heappop(q)
        if (x, y) == target and length >= min:
            return heat

        # make sure we haven't visited this node already
        if ((x, y), (dx, dy), length) in seen:
            continue
        seen.add(((x, y), (dx, dy), length))

        if length >= min and (x+dy, y-dx) in G:
            heapq.heappush(q, (heat + G[(x+dy, y-dx)], (x+dy, y-dx), (dy, -dx), 1))
        if length >= min and (x-dy, y+dx) in G:
            heapq.heappush(q, (heat + G[(x-dy, y+dx)], (x-dy, y+dx), (-dy, dx), 1))
        if length < max and (x+dx, y+dy) in G:
            heapq.heappush(q, (heat + G[(x+dx, y+dy)], (x+dx, y+dy), (dx, dy), length + 1))

print("Answer 1:", dijkstra((0, 0), (x, y), 1, 3))
print("Answer 2:", dijkstra((0, 0), (x, y), 4, 10))
