import re
import math
from itertools import product

d = [(dx, dy) for dx, dy in product((-1, 0, 1), repeat=2) if (dx, dy) != (0, 0)]

with open("./input.txt") as f:
    lines = [[int(n) for n in re.findall(r"-?\d+", line)] for line in f.read().strip().splitlines()]

maxx, maxy = 101, 103

def score(points):
    q = [0, 0, 0, 0]
    for x, y in points:
        if x < maxx // 2:
            if y < maxy // 2:
                q[0] += 1
            elif y > maxy // 2:
                q[1] += 1
        elif x > maxx // 2:
            if y < maxy // 2:
                q[2] += 1
            elif y > maxy // 2:
                q[3] += 1

    return math.prod(q)

points = []
for x, y, dx, dy in lines:
    points.append(((x + dx * 100) % maxx, (y + dy * 100) % maxy))

print("Answer 1:", score(points))

def find_line(points):
    for dx, dy in d:
        for x, y in points:
            isline = True
            for i in range(10):
                if (x + dx * i, y + dy * i) not in points:
                    isline = False
                    break
            if isline:
                return True
    return False

i = 1
while True:
    points = set()
    for x, y, dx, dy in lines:
        points.add(((x + dx * i) % maxx, (y + dy * i) % maxy))
    if find_line(points):
        print("Answer 2:", i)
        break
    i += 1
