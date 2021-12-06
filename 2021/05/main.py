from collections import defaultdict

with open("./input.txt") as f:
    lines = [tuple((lambda c1, c2: (int(c1), int(c2)))(*coord.split(",")) for coord in row.split(" -> ")) for row in f.read().strip().splitlines()]

def isaxis(line):
    return line[0][0] == line[1][0] or line[0][1] == line[1][1]

def part1(lines):
    points = defaultdict(lambda:0)
    for ((x1, y1), (x2, y2)) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                points[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                points[(x, y1)] += 1

    return len([k for k, v in points.items() if v > 1])

print("Answer 1:", part1([l for l in lines if isaxis(l)]))

def part2(lines):
    points = defaultdict(lambda:0)
    for ((x1, y1), (x2, y2)) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                points[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                points[(x, y1)] += 1
        else:
            xi = 1 if x2 > x1 else -1
            yi = 1 if y2 > y1 else -1
            for i in range(abs(x2-x1)+1):
                points[(x1 + xi*i, y1 + yi*i)] += 1

    return len([k for k, v in points.items() if v > 1])

print("Answer 2:", part2(lines))
