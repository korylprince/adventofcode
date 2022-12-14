from itertools import pairwise

from PIL import Image

with open("./input.txt") as f:
    lines = [[tuple(int(n) for n in coords.strip().split(",")) for coords in line.strip().split(" -> ")] for line in f.read().strip().splitlines()]


def fullrange(a, b):
    if a == b:
        yield a
        return
    step = abs(b-a)//(b-a)
    c = a
    while c != b:
        yield c
        c += step
    yield b

G = set()

for l in lines:
    for (x1, y1), (x2, y2) in pairwise(l):
        for x in fullrange(x1, x2):
            for y in fullrange(y1, y2):
                G.add((x, y))

def grain(G, start, target_depth):
    g = start
    while True:
        if g[1] == target_depth:
            return g
        if (next := (g[0], g[1]+1)) not in G:
            g = next
            continue
        if (next := (g[0]-1, g[1]+1)) not in G:
            g = next
            continue
        if (next := (g[0]+1, g[1]+1)) not in G:
            g = next
            continue
        return g

start = (500, 0)
grains = set()
target_depth = max([y for x, y in G])
while True:
    end = grain(G, start, target_depth)
    if end[1] == target_depth:
        break
    G.add(end)
    grains.add(end)

print("Answer 1:", len(grains))

while True:
    end = grain(G, start, target_depth+1)
    G.add(end)
    grains.add(end)
    if end == start:
        break

print("Answer 2:", len(grains))

def write_image(output, G, grains):
    boundaries = (
        (min([x for x, y in G]),
        max([x for x, y in G])),
        (min([y for x, y in G]),
        max([y for x, y in G])),
    )

    img = Image.new("RGB", (boundaries[0][1] - boundaries[0][0] + 1, boundaries[1][1] - boundaries[1][0] + 1), "black")
    pixels = img.load() # Create the pixel map
    for x, y in G:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (255, 255, 255)
    for x, y in grains:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (194, 178, 128)

    img.save(output)

write_image("./output.bmp", G, grains)
