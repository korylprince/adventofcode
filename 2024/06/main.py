G = {}

start_dir = (0, -1)
start = (0, 0)

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char == "^":
                start = (x, y)
                G[(x, y)] = "." 
            else:
                G[(x, y)] = char

dx, dy = start_dir
x, y = start

seen = set()
while True:
    newx, newy = x + dx, y + dy
    if (newx, newy) not in G:
        break

    if G[(newx, newy)] == "#":
        dx, dy = -dy, dx
        continue

    x, y = newx, newy
    seen.add((x, y))

print("Answer 1:", len(seen))

# can't put obstruction at start
seen.remove(start)
loops = set()
for extra in seen:
    dx, dy = start_dir
    x, y = start

    path = set()
    while True:
        newx, newy = x + dx, y + dy
        if (newx, newy) not in G:
            break

        if G[(newx, newy)] == "#" or (newx, newy) == extra:
            dx, dy = -dy, dx
            continue

        x, y = newx, newy

        if ((x, y), (dx, dy)) in path:
            loops.add(extra)
            break

        path.add(((x, y), (dx, dy)))

print("Answer 2:", len(loops))
