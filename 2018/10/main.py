import math
import os
import re
import sys

inputRegexp = "position=<(.*),(.*)> velocity=<(.*),(.*)>"

def getPoints():
    points = []
    with open("./input.txt") as f:
        for line in f.read().splitlines():
            g = re.search(inputRegexp, line).groups()
            points.append(([int(g[0]), int(g[1])], (int(g[2]), int(g[3]))))
    return points

def dot(p1, p2):
    if abs(p2[1] - p1[1]) == 0 and abs(p2[0] - p1[0]) == 0:
        return True
    return False

def draw(output, points):
    points = [p[0] for p in points]
    boundaries = (
        (min([p[0] for p in points]),
         max([p[0] for p in points])),
        (min([p[1] for p in points]),
         max([p[1] for p in points])),
    )

    boundaries = (
        (boundaries[0][0] - (boundaries[0][1] - boundaries[0][0]) * 0.1,
        boundaries[0][1] + (boundaries[0][1] - boundaries[0][0]) * 0.1),
        (boundaries[1][0] - (boundaries[1][1] - boundaries[1][0]) * 0.25,
        boundaries[1][1] + (boundaries[1][1] - boundaries[1][0]) * 0.25),
    )

    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(int(columns)/3)
    xsize = (boundaries[0][1] - boundaries[0][0]) / int(columns)
    if xsize < 0.25:
        xsize =0.25 
    ysize = (boundaries[1][1] - boundaries[1][0]) / int(rows)
    if ysize < 1:
        ysize = 1

    for y in range(int(boundaries[1][0]/ysize), int(boundaries[1][1]/ysize)):
        for x in range(int(boundaries[0][0]/xsize), int(boundaries[0][1]/xsize)):
            point = False
            for p in points:
                if dot((x, y), (int(p[0]/xsize), int(p[1]/ysize))):
                    point = True
                    break
            if point:
                output.write("#")
            else:
                output.write(".")

        output.write("\n")

def move(points):
    for p in points:
        p[0][0] += p[1][0]
        p[0][1] += p[1][1]

def distance(points):
    d = 0
    center = (
        sum([p[0][0] for p in points]) / len(points),
        sum([p[0][1] for p in points]) / len(points),
    )
    for p in points:
        d += math.sqrt(abs((center[0] - p[0][0])**2) + abs((center[1] - p[0][1])**2))

    return d

points1 = getPoints()
points2= getPoints()

move(points1)
d1 = distance(points1)
d2 = distance(points2)

i = 0

#converge points
while d1 < d2:
    move(points1)
    move(points2)
    d1 = distance(points1)
    d2 = distance(points2)
    i += 1

draw(sys.stdout, points2)
print("Seconds:", i)
