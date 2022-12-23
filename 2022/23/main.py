from collections import defaultdict, deque

G = set()

dirs = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
checks = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, c in enumerate(line.strip()):
            if c == "#":
                G.add((x, y))


def round(G):
    moves = defaultdict(list)

    count = 0
    for x, y in G:
        if sum([(x+dx, y+dy) in G for dx, dy in dirs]) == 0:
            count += 1
            continue

        for dx, dy in checks:
            if sum([(x+dx1, y+dy1) in G for dx1, dy1 in dirs if (dx == 0 or dx1 == dx) and (dy == 0 or dy1 == dy)]) == 0:
                moves[(x+dx, y+dy)].append((x, y))
                break

    for target, candidates in moves.items():
        if len(candidates) == 1:
            G.add(target)
            G.remove(candidates[0])

    checks.rotate(-1)
    return count == len(G)

for _ in range(10):
    round(G)

minx = min([x for x, y in G])
maxx = max([x for x, y in G])
miny = min([y for x, y in G])
maxy = max([y for x, y in G])
count = sum([(x, y) not in G for x in range(minx, maxx+1) for y in range(miny, maxy+1)])
print("Answer 1:", count)

count = 10
while not round(G):
    count += 1

print("Answer 2:", count+1)
