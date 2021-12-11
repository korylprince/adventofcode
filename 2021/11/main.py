from collections import defaultdict

with open("./input.txt") as f:
    octo = [[int(n) for n in row.strip()] for row in f.read().strip().splitlines()]

rows, cols = len(octo), len(octo[0])

coords = defaultdict(lambda: -(2**16), {(x, y): octo[y][x] for x in range(cols) for y in range(rows)})

d = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))

def step(coords):
    flash = []
    for y in range(rows):
        for x in range(cols):
            coords[(x, y)] += 1
            if coords[(x, y)] == 10:
                flash.append((x, y))

    count = 0
    while len(flash) > 0:
        count += len(flash)
        next_flash = []
        for x, y in flash:
            for dx, dy in d:
                coords[(x+dx, y+dy)] += 1
                if coords[(x+dx, y+dy)] == 10:
                    next_flash.append((x+dx, y+dy))
        flash = next_flash

    for y in range(rows):
        for x in range(cols):
            if coords[(x, y)] > 9:
                coords[(x, y)] = 0

    return count

print("Answer 1:", sum([step(coords) for i in range(100)]))

steps = 100
while True:
    steps += 1
    if step(coords) == rows * cols:
        break

print("Answer 2:", steps)
