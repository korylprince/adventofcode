import re
import math
from itertools import pairwise, combinations
from collections import defaultdict

G = dict()

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
crossdirs = ((1, 1), (-1, -1), (-1, 1), (1, -1))

with open("./input.txt") as f:
    maptxt, ins = [t for t in f.read().split("\n\n")]
    ins = [int(m) if m.isdigit() else m for m in re.findall(r"(\d+|R|L)", ins)]

start = None

for y, line in enumerate(maptxt.splitlines()):
    for x, c in enumerate(line):
        if start is None and c in (".", "#"):
            start = (x, y)
        if c == " ":
            continue
        G[(x, y)] = c

cur = start
dir = (1, 0)
for i in ins:
    if isinstance(i, int):
        for _ in range(i):
            if (next := (cur[0]+dir[0], cur[1]+dir[1])) not in G:
                wrap = cur
                while True:
                    if (next2 := (wrap[0]-dir[0], wrap[1]-dir[1])) in G:
                        wrap = next2
                    else:
                        break
                if G[wrap] != "#":
                    cur = wrap
                else:
                    break
            elif G[next] == "#":
                break
            else:
                cur = next
    elif i == "R":
        dir = (-dir[1], dir[0])
    elif i == "L":
        dir = (dir[1], -dir[0])

print("Answer 1:", 1000*(cur[1]+1) + 4 * (cur[0]+1) + dirs.index(dir))

# find tiles
G2 = defaultdict(set)
for idx, (y1, y2) in enumerate(pairwise(range(0, len(maptxt.splitlines())+1, 50))):
    for jdx, (x1, x2) in enumerate(pairwise(range(0, len(maptxt.splitlines()[0])+1, 50))):
        for y in range(y1, y2):
            for x in range(x1, x2):
                if (x, y) in G:
                    G2[(jdx, idx)].add((x, y))

# map tile numbers to tile points and vice versa
G3 = {
    1: (1, 0),
    2: (2, 0),
    3: (1, 1),
    4: (0, 2),
    5: (1, 2),
    6: (0, 3),
    (1, 0): 1,
    (2, 0): 2,
    (1, 1): 3,
    (0, 2): 4,
    (1, 2): 5,
    (0, 3): 6,
}

# map translations; bool notates if edges are mapped in reverse
gmap = {
    (1, (0, -1)): (6, (1, 0), False),
    (1, (-1, 0)): (4, (1, 0), True),

    (2, (1, 0)): (5, (-1, 0), True),
    (2, (0, 1)): (3, (-1, 0), False),
    (2, (0, -1)): (6, (0, -1), False),

    (3, (1, 0)): (2, (0, -1), False),
    (3, (-1, 0)): (4, (0, 1), False),

    (4, (0, -1)): (3, (1, 0), False),
    (4, (-1, 0)): (1, (1, 0), True),

    (5, (1, 0)): (2, (-1, 0), True),
    (5, (0, 1)): (6, (-1, 0), False),

    (6, (-1, 0)): (1, (0, 1), False),
    (6, (0, 1)): (2, (0, 1), False),
    (6, (1, 0)): (5, (0, -1), False),
}

# return tile edge based on direction
def edge(tile, e):
    points = G2[G3[tile]]
    minx = min([x for x, y in points])
    maxx = max([x for x, y in points])
    miny = min([y for x, y in points])
    maxy = max([y for x, y in points])
    match e:
        case (1, 0):
            return sorted([(x, y) for x, y in points if x == maxx])
        case (-1, 0):
            return sorted([(x, y) for x, y in points if x == minx])
        case (0, 1):
            return sorted([(x, y) for x, y in points if y == maxy])
        case (0, -1):
            return sorted([(x, y) for x, y in points if y == miny])


# map edge point to edge point
wrapmap = {}
s = set()
for (t1, d1), (t2, d2, r) in gmap.items():
    t1e = edge(t1, d1)
    t2e = edge(t2, (-d2[0], -d2[1]))
    if r:
        t2e = list(reversed(t2e))
    wrapmap.update(dict(zip(zip(t1e, (d1,)*len(t1e)), t2e)))


# run through instructions
cur = start
dir = (1, 0)
for i in ins:
    if isinstance(i, int):
        for _ in range(i):
            if (next := (cur[0]+dir[0], cur[1]+dir[1])) not in G:
                curtile = G3[[coords for coords, s in G2.items() if cur in s][0]]
                tile, nextdir, _ = gmap[(curtile, dir)]
                next = wrapmap[(cur, dir)]
                if G[next] != "#":
                    cur = next
                    dir = nextdir
                else:
                    break
            elif G[next] == "#":
                break
            else:
                cur = next
    elif i == "R":
        dir = (-dir[1], dir[0])
    elif i == "L":
        dir = (dir[1], -dir[0])

print("Answer 2:", 1000*(cur[1]+1) + 4 * (cur[0]+1) + dirs.index(dir))
