from collections import defaultdict
import heapq

# parse grid
valid = set()
G = defaultdict(set)
with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if y == 0 and c == ".":
                start = (x, y)
            elif y == len(lines) - 1 and c == ".":
                target = (x, y)
            if c in (".><v^"):
                valid.add((x, y))
                if c != ".":
                    G[c].add((x, y))

# find bounds
minx = min([x for x, y in valid])
maxx = max([x for x, y in valid])
miny = min([y for x, y in valid.difference(set((start, target)))])
maxy = max([y for x, y in valid.difference(set((start, target)))])

dirs = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}

# play out blizzards for several rounds
blizz = {0: G}
blocked = {0: set.union(*list(G.values()))}
for idx in range(1, 1000):
    new = defaultdict(set)
    for dir, (dx, dy) in dirs.items():
        for x, y in blizz[idx-1].get(dir, set()):
            if (next := (x+dx, y+dy)) in valid:
                new[dir].add(next)
            else:
                match dx, dy:
                    case (1, 0):
                        new[dir].add((minx, y))
                    case (-1, 0):
                        new[dir].add((maxx, y))
                    case (0, 1):
                        new[dir].add((x, miny))
                    case (0, -1):
                        new[dir].add((x, maxy))
    blizz[idx] = new
    blocked[idx] = set.union(*list(new.values()))

dirs = tuple(dirs.values()) + ((0, 0),)

# bfs paths
def bfs(valid, blocked, start, target):
    # minute, node
    heap = [start]
    heapq.heapify(heap)
    seen = set()
    while len(heap) > 0:
        minute, node = heapq.heappop(heap)
        
        if node == target:
            return minute

        for dx, dy in dirs:
            next = (node[0]+dx, node[1]+dy)
            if next in valid and next not in blocked[minute+1]:
                if (nextnode := (minute+1, next)) not in seen:
                    heapq.heappush(heap, nextnode)
                    seen.add(nextnode)

m = bfs(valid, blocked, (0, start), target)
print("Answer 1:", m)
m = bfs(valid, blocked, (m, target), start)
m = bfs(valid, blocked, (m, start), target)
print("Answer 2:", m)
