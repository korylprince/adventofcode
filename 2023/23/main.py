import heapq
from collections import defaultdict
from itertools import pairwise

Grid = dict()

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char != "#":
                Grid[(x, y)] = char

maxx, maxy = x, y
source = ([x for x, y in Grid if y == 0][0], 0)
target = ([x for x, y in Grid if y == maxy][0], maxy)

downdirs = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

def dijkstra(source, target):
    # -steps, x, y, seen
    q = [(0, source[0], source[1], set())]
    all_seen = defaultdict(lambda:0)
    heapq.heapify(q)
    max = 0
    while len(q) > 0:
        steps, x, y, seen = heapq.heappop(q)
        if (x, y) == target:
            if -steps > max:
                max = -steps
                continue
        if (x, y) in seen:
            continue
        seen.add((x, y))

        # filter out bad weights to make this converge quicker
        if all_seen[(x, y)] > (-steps) * 1.5:
            continue
        all_seen[(x, y)] = -steps

        if (dir := Grid[(x, y)]) in downdirs:
            dx, dy = downdirs[dir]
            if (x+dx, y+dy) in Grid:
                heapq.heappush(q, (steps - 1, x+dx, y+dy, seen))
            continue

        for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            if (x+dx, y+dy) in Grid:
                if (dir := (x+dx, y+dy)) in downdirs and downdirs[dir] == (dx, dy):
                    continue
                newseen = seen.copy()
                heapq.heappush(q, (steps - 1, x+dx, y+dy, newseen))
    return max

print("Answer 1:", dijkstra(source, target))

# create neighbors mapping
N = defaultdict(set)
for x, y in Grid:
    for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
        if (x+dx, y+dy) in Grid:
            N[(x, y)].add((x+dx, y+dy))

# create neighbor lengths for non-line neighbors
G = dict()
for node in Grid:
    neighbors = N[node]
    if len(neighbors) > 2:
        for n in neighbors:
            G[frozenset([node, n])] = 1

# compress line neighbors
left = set(node for node, n in N.items() if len(n) == 2)
while len(left) > 0:
    node = left.pop()
    line = set()
    q = [node]
    ends = set()
    weight = 0
    while len(q) > 0:
        n = q.pop()
        line.add(n)
        for neighbor in N[n]:
            if (f := frozenset([n, neighbor])) in G:
                del G[f]
            if neighbor in line:
                continue
            if len(N[neighbor]) == 2:
                q.append(neighbor)
                weight += 1
            else:
                weight += 1
                ends.add(neighbor)
    left.difference_update(line)
    G[frozenset(ends)] = weight

# recreate neighbor mapping with compressed neighbors
N = defaultdict(set)
for neighbors in G:
    for n1, n2 in pairwise(neighbors):
        N[n1].add(n2)
        N[n2].add(n1)

def dijkstra2(N, G, source, target):
    # steps, node, seen
    q = [(0, source, set())]
    all_seen = defaultdict(lambda:0)
    heapq.heapify(q)
    max = 0
    while len(q) > 0:
        weight, node, seen = heapq.heappop(q)
        if node == target:
            if -weight > max:
                max = -weight
            continue
        if node in seen:
            continue
        seen.add(node)

        # filter out really bad weights to make this converge quickly
        if all_seen[node] > (-weight) * 2:
            continue
        all_seen[node] = -weight

        for neighbor in N[node]:
            newseen = seen.copy()
            heapq.heappush(q, (weight - G[frozenset([node, neighbor])], neighbor, newseen))

    return max

print("Answer 2:", dijkstra2(N, G, source, target))
