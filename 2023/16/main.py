from collections import deque

G = dict()
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            G[(x, y)] = char
maxx, maxy = x, y

def bfs(G, x, y, dx, dy):
    q = deque([(x, y, dx, dy)])
    seen = set()
    while len(q):
        x, y, dx, dy = q.popleft()
        if (x, y) not in G:
            continue

        if (x, y, dx, dy) in seen:
            continue
        seen.add((x, y, dx, dy))

        char = G[(x, y)]
        if char == "\\":
            if dy == 0:
                dx, dy = -dy, dx
            else:
                dx, dy = dy, -dx
        elif char == "/":
            if dx == 0:
                dx, dy = -dy, dx
            else:
                dx, dy = dy, -dx

        if char in "./\\":
            q.append((x+dx, y+dy, dx, dy))
            continue

        if dy == 0 and char == "|":
            q.append((x, y-1, 0, -1))
            q.append((x, y+1, 0, 1))
        elif dx == 0 and char == "-":
            q.append((x-1, y, -1, 0))
            q.append((x+1, y, 1, 0))
        else:
            q.append((x+dx, y+dy, dx, dy))

    return len(set((x, y) for x, y, _, _ in seen))

max = bfs(G, 0, 0, 1, 0)
print("Answer 1:", max)

for y in range(maxy+1):
    if (m := bfs(G, 0, y, 1, 0)) > max:
        max = m
    if (m := bfs(G, maxx, y, -1, 0)) > max:
        max = m

for x in range(maxx+1):
    if (m := bfs(G, x, 0, 0, 1)) > max:
        max = m
    if (m := bfs(G, x, maxy, 0, -1)) > max:
        max = m

print("Answer 2:", max)
