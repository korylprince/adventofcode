import re
from itertools import pairwise, combinations

# manhattan distance
def d(a, b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

# find corners of boundary
def corners(sensor, dis):
    return ((sensor[0] - dis, sensor[1]), (sensor[0], sensor[1] - dis),
               (sensor[0] + dis, sensor[1]), (sensor[0], sensor[1] + dis))

# find point slope for bounding lines
def lines(corners):
    lines = []
    for a, b in list(pairwise(corners)) + [(corners[-1], corners[0])]:
        slope = (b[1] - a[1])//(b[0] - a[0])
        xint = slope * -a[0] + a[1]
        lines.append((a, b, slope, xint))
    return lines


with open("./input.txt") as f:
    sensors = [[int(n) for n in re.findall(r"\-?\d+", line)] for line in f.read().strip().splitlines()]
    sensors = [((x1, y1), (x2, y2)) for x1, y1, x2, y2 in sensors]
    sensors = [(*s, d(*s), corners(s[0], d(*s))) for s in sensors]
    sensors = [(*s, lines(s[3])) for s in sensors]
    # (sensor(x, y), beacon(x, y), d(s, b), []corners(x, y), []lines(a, b, m, x-int))

target = 2_000_000
targetbeacons = len(set([s[1][0] for s in sensors if s[1][1] == target]))

# find intersections with target line
ranges = []
for idx, s in enumerate(sensors):
    ys = [y for x, y in s[3]]
    if min(ys) <= target <= max(ys):
        diff = s[2] - abs(target - s[0][1])
        ranges.append((s[0][0] - diff, s[0][0] + diff))


# count all overlapping regions
queue = sorted(sum([[("start", r1), ("stop", r2)] for r1, r2 in ranges], []), key=lambda r: r[1])
level = 0
cur = queue[0][1] - 1
count = 1 # count 0th index
for ss, n in queue:
    if level > 0:
        count += n - cur
    if ss == "start":
        level += 1
    else:
        level -= 1
    cur = n

print("Answer 1:", count - targetbeacons)

# finds integer intersections between two lines with slope 1 and -1
def intersect(l1, l2):
    if l1[2] == l2[2]:
        return None
    if l1[2] == -1:
        x = (l1[3] - l2[3]) / 2
        y = (l1[3] + l2[3]) / 2
    else:
        x = (l2[3] - l1[3]) / 2
        y = (l2[3] + l1[3]) / 2
    if x // 1 != x or y // 1 != y:
        return None
    return int(x), int(y)

# find all intersections
intersections = set()
for s1, s2 in combinations(sensors, 2):
    for l1 in s1[4]:
        for l2 in s2[4]:
            if (i := intersect(l1, l2)) is not None:
                intersections.add(i)

# search near intersections for point not contained by any sensor bounds
def part2():
    maxbounds = 4_000_000
    for x, y in intersections:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if not (0 <= x+dx <= maxbounds) or not (0 <= y+dy <= maxbounds):
                continue
            found = False
            for s in sensors:
                if d(s[0], (x+dx, y+dy)) <= d(s[0], s[1]):
                    found = True
                    break
            if not found:
                return (x+dx) * 4_000_000 + (y+dy)

print("Answer 2:", part2())
