from collections import defaultdict
import queue
import heapq

import networkx as nx

grid = {}
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c

BLOCK_WALL = "#"
BLOCK_ME = "@"
BLOCK_KEYS =  [chr(o) for o in range(ord("a"), ord("z") + 1) if chr(o) in grid.values()]
BLOCK_DOORS = [chr(o) for o in range(ord("A"), ord("Z") + 1) if chr(o) in grid.values()]

def bfs_cache(grid, source, targets):
    cache = defaultdict(lambda:{})
    for t in [source] + targets:
        seen = set([t] + [k for k, v in grid.items() if v == BLOCK_WALL])
        q = queue.Queue()
        q.put(([t], []))
        while not q.empty():
            path, doors = q.get()
            pos = path[-1]
            for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (new := (pos[0] + d[0], pos[1] + d[1])) not in seen:
                    seen.add(new)
                    if (door := grid[new]) in BLOCK_DOORS:
                        doors = doors + [door]
                    if new in targets:
                        cache[t][new] = (grid[new], len(path), set([d.lower() for d in doors]))
                    q.put((path + [new], doors))

    return cache


def dijkstra(cache, source):
    seen = defaultdict(lambda:2**32)
    heap = [(0, source, [])]
    while len(heap) > 0:
        length, pos, collected = heapq.heappop(heap)
        if len(collected) == len(BLOCK_KEYS):
            return length
        for new, (key, l, required) in sorted(cache[pos].items(), key=lambda x: x[1][1]):
            if key in collected or len([r for r in required if r not in collected]) > 0:
                continue

            new_collected = sorted(collected + [key])
            if seen[(seen_key := (new, tuple(new_collected)))] <= length + l:
                continue
            seen[seen_key] = length + l

            heapq.heappush(heap, (length + l, new, new_collected))


def dijkstra2(cache, entrances):
    seen = defaultdict(lambda:2**32)
    heap = [(0, tuple(entrances), [])]
    while len(heap) > 0:
        length, positions, collected = heapq.heappop(heap)
        if len(collected) == len(BLOCK_KEYS):
            return length
        for i, pos in enumerate(positions):
            for new, (key, l, required) in sorted(cache[pos].items(), key=lambda x: x[1][1]):
                if key in collected or len([r for r in required if r not in collected]) > 0:
                    continue

                new_collected = sorted(collected + [key])
                if seen[(seen_key := (positions[:i] + (new,) + positions[i+1:], tuple(new_collected)))] <= length + l:
                    continue
                seen[seen_key] = length + l

                heapq.heappush(heap, (length + l, positions[:i] + (new,) + positions[i+1:], new_collected))


me = [k for k, v in grid.items() if v == BLOCK_ME][0]
keys = [k for k, v in grid.items() if v in BLOCK_KEYS]

cache = bfs_cache(grid, me, keys)
length = dijkstra(cache, me)
print("Answer 1:", length)


grid = {}
with open("./input2.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c

entrances = [k for k, v in grid.items() if v == BLOCK_ME]
cache = {}
for e in entrances:
    cache.update(bfs_cache(grid, e, keys))

length = dijkstra2(cache, entrances)
print("Answer 2:", length)
