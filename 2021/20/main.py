from collections import defaultdict

with open("./input.txt") as f:
    alg, img = f.read().strip().split("\n\n")
    alg = [1 if c == "#" else 0 for c in alg.strip()]
    # (x, y) -> pixel
    img = defaultdict(lambda: 0, {(x, y): 1 if c == "#" else 0 for y, row in enumerate(img.strip().splitlines()) for x, c in enumerate(row.strip())})


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

default = 0

for i in range(2):
    img2 = defaultdict(lambda: default)
    grow(img, default)
    keys = list(img.keys())
    for x, y in keys:
        idx = ((img[(x-1, y-1)] << 8) + (img[(x, y-1)] << 7) + (img[(x+1, y-1)] << 6) +
            (img[(x-1, y)] << 5) + (img[(x, y)] << 4) + (img[(x+1, y)] << 3) +
            (img[(x-1, y+1)] << 2) + (img[(x, y+1)] << 1) + img[(x+1, y+1)])
        img2[(x, y)] = alg[idx]
    img = img2
    default = 0 if default else 1

print("Answer 1:", sum(img.values()))

for i in range(48):
    img2 = defaultdict(lambda: default)
    grow(img, default)
    keys = list(img.keys())
    for x, y in keys:
        idx = ((img[(x-1, y-1)] << 8) + (img[(x, y-1)] << 7) + (img[(x+1, y-1)] << 6) +
            (img[(x-1, y)] << 5) + (img[(x, y)] << 4) + (img[(x+1, y)] << 3) +
            (img[(x-1, y+1)] << 2) + (img[(x, y+1)] << 1) + img[(x+1, y+1)])
        img2[(x, y)] = alg[idx]
    img = img2
    default = 0 if default else 1

print("Answer 2:", sum(img.values()))
