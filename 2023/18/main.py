import re
from itertools import pairwise

dirs = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}

with open("./input.txt") as f:
    ins = [re.match(r"([RLUD]) (\d+) \((.*)\)", line).groups() for line in f.read().strip().splitlines()]
    ins = [(x, int(y), z) for x, y, z in ins]

def shoelaceArea(pts):
    sum1 = pts[len(pts)-1][0]*pts[0][1]
    sum2 = pts[0][0]*pts[len(pts)-1][1]

    for i in range(0,len(pts)-1):
        sum1 = sum1 + pts[i][0] *  pts[i+1][1]
        sum2 = sum2 + pts[i][1] *  pts[i+1][0]

    area = abs(sum1 - sum2) / 2
    return area

def points(ins):
    cur = (0, 0)
    corners = []
    for dir, num in ins:
        dx, dy = dirs[dir]
        cur = (cur[0] + num*dx, cur[1] + num*dy)
        corners.append(cur)
    return corners

def perimeter(pts):
    p = len(pts)
    for (x1, y1), (x2, y2) in pairwise(pts + [pts[0]]):
        p += abs(x1 - x2) + abs(y1 - y2) - 1
    return p

def solve(ins):
    pts = points(ins)
    # picks theorem
    # I = S - B/2 + 1
    area = shoelaceArea(pts) 
    per = perimeter(pts)
    insidepts = area - per // 2 + 1
    return int(insidepts + per)

def parse(h):
    d = {"0": "R", "1": "D", "2": "L", "3": "U"}
    return d[h[-1]], int(h[1:-1], 16)

# use instructions to get points
# calculate perimeter from points
# calculate area from points using Shoelace formula
# calculate inside points with picks theorem
# answer is perimeter + inside points

print("Answer 1:", solve([(dir, num) for dir, num, _ in ins]))
print("Answer 2:", solve([parse(color) for _, _, color in ins]))
