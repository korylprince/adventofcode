from collections import defaultdict

with open("./input.txt") as f:
    alg, img = f.read().strip().split("\n\n")
    alg = list(alg.strip())
    # (x, y) -> pixel
    img = defaultdict(lambda: ".", {(x, y): c for y, row in enumerate(img.strip().splitlines()) for x, c in enumerate(row.strip())})

d = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (0, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1),
)

def grow(img, default):
    x1 = min([x for x, y in img.keys()])
    x2 = max([x for x, y in img.keys()])
    y1 = min([y for x, y in img.keys()])
    y2 = max([y for x, y in img.keys()])
    for x in range(x1-1, x2+2):
        img[(x, y1-1)] = default
        img[(x, y2+1)] = default

    for y in range(y1-1, y2+2):
        img[(x1-1, y)] = default
        img[(x2+1, y)] = default

def p2num(img, x, y):
    n = 0 
    for idx, (dx, dy) in enumerate(d):
        if img[(x+dx, y+dy)] == "#":
            n += 1 << (len(d) - 1 - idx)
    return n

default = "."

for i in range(2):
    img2 = defaultdict(lambda: default)
    grow(img, default)
    keys = list(img.keys())
    for x, y in keys:
        img2[(x, y)] = alg[p2num(img, x, y)]
    img = img2
    default = "#" if default == "." else "."

print("Answer 1:", len([v for v in img.values() if v == "#"]))

for i in range(48):
    img2 = defaultdict(lambda: default)
    grow(img, default)
    keys = list(img.keys())
    for x, y in keys:
        img2[(x, y)] = alg[p2num(img, x, y)]
    img = img2
    default = "#" if default == "." else "."

print("Answer 2:", len([v for v in img.values() if v == "#"]))
