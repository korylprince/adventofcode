from collections import defaultdict
from itertools import product

grid = defaultdict(lambda:".")
Xs = set()
As = set()

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            grid[(x, y)] = char
            if char == "X":
                Xs.add((x, y))
            elif char == "A":
                As.add((x, y))


dirs = [(dx, dy) for dx, dy in product((-1, 0, 1), repeat=2) if (dx, dy) != (0, 0)]

count = 0
for x, y in Xs:
    for dx, dy in dirs:
        if tuple(grid[(x+dx*i, y+dy*i)] for i in range(4)) == tuple("XMAS"):
            count += 1

print("Answer 1:", count)

count = 0
matches = {"MS", "SM"}
for x, y in As:
    if grid[(x+1, y+1)] + grid[(x-1, y-1)] in matches and grid[(x-1, y+1)] + grid[(x+1, y-1)] in matches:
        count += 1

print("Answer 2:", count)
