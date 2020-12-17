import itertools
from collections import defaultdict

INACTIVE = "."
ACTIVE = "#"

d = tuple(d for d in itertools.product((-1, 0, 1), repeat=3) if d != (0, 0, 0))

G = defaultdict(lambda:INACTIVE)

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            G[(x, y, 0)] = char

def cycle(G):
    # grow
    grow = {}
    for x, y, z in list(G.keys()):
        for dx, dy, dz in d:
            if (coords := (x+dx, y+dy, z+dz)) not in G:
                grow[coords] = INACTIVE
    G.update(grow)

    update = {}
    for (x, y, z), status in list(G.items()):
        active = len([None for dx, dy, dz in d if G[(x+dx, y+dy, z+dz)] == ACTIVE])
        if status == ACTIVE and (active != 2 and active != 3):
            update[(x, y, z)] = INACTIVE
        if status == INACTIVE and active == 3:
            update[(x, y, z)] = ACTIVE
    G.update(update)

for i in range(6):
    cycle(G)

print("Answer 1:", list(G.values()).count(ACTIVE))

d = tuple(d for d in itertools.product((-1, 0, 1), repeat=4) if d != (0, 0, 0, 0))

G = defaultdict(lambda:INACTIVE)

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            G[(x, y, 0, 0)] = char

def cycle4(G):
    # grow
    grow = {}
    for x, y, z, w in list(G.keys()):
        for dx, dy, dz, dw in d:
            if (coords := (x+dx, y+dy, z+dz, w+dw)) not in G:
                grow[coords] = INACTIVE
    G.update(grow)

    update = {}
    for (x, y, z, w), status in list(G.items()):
        active = len([None for dx, dy, dz, dw in d if G[(x+dx, y+dy, z+dz, w+dw)] == ACTIVE])
        if status == ACTIVE and (active != 2 and active != 3):
            update[(x, y, z, w)] = INACTIVE
        if status == INACTIVE and active == 3:
            update[(x, y, z, w)] = ACTIVE
    G.update(update)

for i in range(6):
    cycle4(G)

print("Answer 2:", list(G.values()).count(ACTIVE))
