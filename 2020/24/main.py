import re
from collections import defaultdict

def parse(line):
    dirs = []
    pre = ""
    for c in line:
        if c in ("s", "n"):
            pre = c
        else:
            dirs.append(pre + c)
            pre = ""
    return dirs

with open("./input.txt") as f:
    insts = [parse(line.strip()) for line in f.read().strip().splitlines()]

dirs = {
    "e": (2, 0),
    "w": (-2, 0),
    "ne": (1, 1),
    "nw": (-1, 1),
    "se": (1, -1),
    "sw": (-1, -1),
}

def path(input):
    (x, y) = (0, 0)
    for dir in input:
        dx, dy = dirs[dir]
        x, y = (x+dx, y+dy)
    return x, y


tiles = set()

for i in insts:
    p = path(i)
    if p in tiles:
        tiles.remove(p)
    else:
        tiles.add(p)

print("Answer 1:", len(tiles))

for l in range(100):
    check = tiles.copy()
    check2 = set()
    for x, y in check:
        for dx, dy in dirs.values():
            check2.add((x+dx, y+dy))
    check.update(check2)

    black = []
    white = []
    for x, y in check:
        found = len([None for dx, dy in dirs.values() if (x+dx, y+dy) in tiles])

        if (x, y) in tiles and (found == 0 or found > 2):
            white.append((x, y))
        elif (x, y) not in tiles and found == 2:
            black.append((x, y))

    for x, y in white:
        tiles.remove((x, y))
    for x, y in black:
        tiles.add((x, y))

print("Answer 2:", len(tiles))
