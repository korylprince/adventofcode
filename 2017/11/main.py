import math
import heapq

dirs = {
    "n": (0, 2),
    "ne": (1, 1),
    "se": (1, -1),
    "s": (0, -2),
    "sw": (-1, -1),
    "nw": (-1, 1),
}

with open("./input.txt") as f:
    ins = [dirs[d] for d in f.read().strip().split(",")]

target = (sum(x for x, y in ins), sum(y for x, y in ins))

def d(a, b):
    return math.sqrt((b[0]-a[0])**2 + ((b[1]-a[1])**2)/3)


# use a star with weighted euclidean distance as heuristic
def astar(target):
    # (steps, distance), node
    heap = [((d((0, 0), target), 0), (0, 0))]
    heapq.heapify(heap)
    seen = set()
    while len(heap) > 0:
        (_, steps), node = heapq.heappop(heap)
        if node == target:
            return steps
        for dx, dy in dirs.values():
            if (next := (node[0]+dx, node[1]+dy)) in seen:
                continue
            seen.add(next)

            heapq.heappush(heap, ((d(next, target), steps + 1), next))

print("Answer 1:", astar(target))


# find the highest 200 distances and search for the most steps within those targets
distances = []
oldtarget = target
target = (0, 0)
for dx, dy in ins:
    target = (target[0]+dx, target[1]+dy)
    if target == oldtarget:
        continue
    distances.append((target, d((0, 0), target)))

distances.sort(key=lambda t: abs(t[1]), reverse=True)

most = 0
for target, _ in distances[:200]:
    steps = astar(target)
    if steps > most:
        most = steps

print("Answer 2:", most)
