from collections import deque

G = {}

with open("./input.txt") as f:
    for y, line in enumerate([line.strip() for line in f.read().strip().splitlines()]):
        for x, char in enumerate(line):
            G[(x, y)] = char

pipe_dirs = {
    "-": ((-1, 0), (1, 0)),
    "|": ((0, -1), (0, 1)),
    "7": ((-1, 0), (0, 1)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "F": ((1, 0), (0, 1)),
}

dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))

start = [coords for coords in G if G[coords] == "S"][0]

# find shape of start
start_dirs = []
for dx, dy in dirs:
    if (coords := (start[0]+dx, start[1]+dy)) not in G or (typ := G[coords]) not in pipe_dirs:
        continue
    if (-dx, -dy) in pipe_dirs[typ]:
        start_dirs.append((dx, dy))
G[start] = [typ for typ, d in pipe_dirs.items() if (start_dirs[0], start_dirs[1]) == d or (start_dirs[1], start_dirs[0]) == d][0]

# dfs loop
def dfs():
    seen = set()
    loop = [start]
    while True:
        (x, y) = loop[-1]
        for dx, dy in pipe_dirs[G[(x, y)]]:
            coords = (x+dx, y+dy)
            if coords == start:
                return loop
            if coords in seen or coords not in G:
                continue
            seen.add(coords)
            loop.append(coords)
            break # make sure and go one direction from the start

loop = deque(dfs())
looptiles = set(loop)
print("Answer 1:", len(loop) // 2)



rotations = {
    "J": {(1, 0): (0, -1), (0, 1): (-1, 0)},
    "L": {(-1, 0): (0, -1), (0, 1): (1, 0)},
    "F": {(-1, 0): (0, 1), (0, -1): (1, 0)},
    "7": {(1, 0): (0, 1), (0, -1): (-1, 0)},
}

# step through loop until (1, 0) vector can be set (i.e. --)
while G[loop[0]] != "-" or G[loop[1]] != "-":
    loop.rotate()

# color along loop
vector = (1, 0)
left = set()
right = set()
q = loop.copy()
while len(q) > 0:
    (x, y) = q.popleft()

    lefttile = (x + vector[1], y - vector[0]) # cw
    righttile = (x - vector[1], y + vector[0]) # ccw
    if lefttile in G and lefttile not in looptiles:
        left.add(lefttile)
    if righttile in G and righttile not in looptiles:
        right.add(righttile)

    # rotate and color other side of corner
    if G[(x, y)] in "JLF7":
        vector = rotations[G[(x, y)]][vector]

        lefttile = (x + vector[1], y - vector[0]) # cw
        righttile = (x - vector[1], y + vector[0]) # ccw
        if lefttile in G and lefttile not in looptiles:
            left.add(lefttile)
        if righttile in G and righttile not in looptiles:
            right.add(righttile)


def floodfill(tiles):
    filled = tiles.copy()
    q = deque(filled)
    bounded = True
    while len(q) > 0:
        (x, y) = q.popleft()
        for dx, dy in dirs:
            coords = (x+dx, y+dy)
            if coords not in G:
                bounded = False
                continue
            if coords in filled or coords in looptiles:
                continue
            filled.add(coords)
            q.append(coords)
    return filled, bounded

# flood fill left/right sides
leftall, leftbounded = floodfill(left)
rightall, rightbounded = floodfill(right)

if leftbounded:
    print("Answer 1:", len(leftall))
elif rightbounded:
    print("Answer 1:", len(rightall))
