import re

claimRegexp = "^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$"

#format (id, (x, y), (l, w))
claims = []

with open("./input.txt") as f:
    for line in f:
        groups = re.match(claimRegexp, line).groups()
        claims.append((groups[0], (int(groups[1]), int(groups[2])), (int(groups[3]), int(groups[4]))))


#claimSquare is 1x1 square represented by top left corner
# id: set(claimSquares...)
claimSquares = {}

for c in claims:
    claimSquares[c[0]] = set()
    for x in range(c[1][0], c[1][0] + c[2][0]):
        for y in range(c[1][1], c[1][1] + c[2][1]):
            claimSquares[c[0]].add((x, y))

#(x, y): count
squareCounts = {}

for c in claimSquares:
    for x, y in claimSquares[c]:
        if (x, y) not in squareCounts:
            squareCounts[(x, y)] = 0
        squareCounts[(x, y)] += 1

total = sum([1 for c in squareCounts if squareCounts[c] > 1])

print("Overlapping in²:", total)

for id, claimsList in claimSquares.items():
    bad = False
    for c in claimsList:
        if squareCounts[c] > 1:
            bad = True
            break
    if bad:
        continue

    print("Non-overlapping ID:", id)
    break
