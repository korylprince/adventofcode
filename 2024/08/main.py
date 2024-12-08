from collections import defaultdict
from itertools import combinations

ant = defaultdict(set)

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char != ".":
                ant[char].add((x, y))

maxx, maxy = x, y

anti = set()
for freq, ants in ant.items():
    for (x1, y1), (x2, y2) in combinations(ants, 2):
        dx, dy = x2 - x1, y2 - y1
        if 0 <= x1-dx <= maxx and 0 <= y1-dy <= maxy:
            anti.add((x1-dx, y1-dy))
        if 0 <= x2+dx <= maxx and 0 <= y2+dy <= maxy:
            anti.add((x2+dx, y2+dy))

print("Answer 1:", len(anti))

anti = set()
for freq, ants in ant.items():
    for (x1, y1), (x2, y2) in combinations(ants, 2):
        dx, dy = x2 - x1, y2 - y1

        xk, yk = x1, y1
        anti.add((xk, yk))
        while  0 <= xk-dx <= maxx and 0 <= yk-dy <= maxy:
            anti.add((xk-dx, yk-dy))
            xk, yk = xk-dx, yk-dy

        xk, yk = x1, y1
        while  0 <= xk+dx <= maxx and 0 <= yk+dy <= maxy:
            anti.add((xk+dx, yk+dy))
            xk, yk = xk+dx, yk+dy

print("Answer 2:", len(anti))
