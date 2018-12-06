with open("./input.txt") as f:
    coords = [(int(line.split(",")[0]), int(line.split(",")[1])) for line in f.read().splitlines()]

boundaries = (
    (min([x for x, y in coords]), max([x for x, y in coords])),
    (min([y for x, y in coords]), max([y for x, y in coords])),
)

def distance(c1, c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])

grid = {}

for x in range(boundaries[0][0], boundaries[0][1]):
    for y in range(boundaries[1][0], boundaries[1][1]):
        distances = {c: distance(c, (x, y)) for c in coords}
        m = [k for k, v in distances.items() if v == min(distances.values())]
        if len(m) == 1:
            grid[(x, y)] = m[0]

gv = list(grid.values())

counts = {c: gv.count(c) for c in set(gv)}


for x in range(boundaries[0][0], boundaries[0][1]):
    c = (x, boundaries[1][0])
    if c in counts:
        del counts[c]

    c = (x, boundaries[1][1])
    if c in counts:
        del counts[c]

for y in range(boundaries[1][0], boundaries[1][1]):
    c = (boundaries[0][0], y)
    if c in counts:
        del counts[c]

    c = (boundaries[0][1], y)
    if c in counts:
        del counts[c]

maxCoord = [c for c, cnt in counts.items() if cnt == max(counts.values())][0]

print("Best coordinate:", maxCoord, "with area:", counts[maxCoord])

grid = set()

for x in range(boundaries[0][0], boundaries[0][1]):
    for y in range(boundaries[1][0], boundaries[1][1]):
        if sum([distance(c, (x, y)) for c in coords]) < 10000:
            grid.add((x, y))

print("Area of region:", len(grid))
