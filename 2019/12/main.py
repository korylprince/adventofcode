import re
import itertools

import numpy as np

planetRe = "<x=([\-0-9]+), y=([\-0-9]+), z=([\-0-9]+)>"

def step(planets):
    for a, b in itertools.combinations(planets, 2):
        for axis in range(3):
            if a[0:3][axis] > b[0:3][axis]:
                a[3:6][axis] -= 1
                b[3:6][axis] += 1
            if b[0:3][axis] > a[0:3][axis]:
                b[3:6][axis] -= 1
                a[3:6][axis] += 1

    for p in planets:
        p[0:3] += p[3:6]

with open("./input.txt") as f:
    groups = [re.match(planetRe, line.strip()).groups() for line in f.read().strip().splitlines()]
    planets = [np.array([int(g[0]), int(g[1]), int(g[2]), 0, 0, 0]) for g in groups]

for i in range(1000):
    step(planets)

energy = sum([sum(abs(p[0:3])) * sum(abs(p[3:6])) for p in planets])
print("Answer 1:", energy)

with open("./input.txt") as f:
    groups = [re.match(planetRe, line.strip()).groups() for line in f.read().strip().splitlines()]
    planets = [np.array([int(g[0]), int(g[1]), int(g[2]), 0, 0, 0]) for g in groups]

count = 0
loopcount = [0, 0, 0]
found = []

start = {}
for i in range(3):
    start[i] = (planets[0][i], planets[0][i+3], planets[1][i], planets[1][i+3], planets[2][i], planets[2][i+3])

while len(found) < len(loopcount):
    step(planets)
    count += 1

    for i in range(3):
        if loopcount[i] == 0:
            if (planets[0][i], planets[0][i+3], planets[1][i], planets[1][i+3], planets[2][i], planets[2][i+3]) == start[i]:
                loopcount[i] = count
                found.append(count)

print("Answer 2:", np.lcm.reduce(found))
