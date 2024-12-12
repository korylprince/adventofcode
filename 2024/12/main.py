from collections import defaultdict

d = ((0, 1), (0, -1), (1, 0), (-1, 0))

G = defaultdict(lambda:None)

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            G[(x, y)] = char

unseen = set(list(G.keys()))

total = 0
total2 = 0

while len(unseen) > 0:
    area = 0
    perimeter = 0

    q = [next(iter(unseen))]
    seen = set()
    typ = G[q[0]]
    edges = set()

    # flood fill
    while len(q) > 0:
        x, y = q.pop()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        area += 1
        unseen.remove((x, y))
        for dx, dy in d:
            newx, newy = x + dx, y + dy
            if G[(newx, newy)] == typ:
                q.append((newx, newy))
            else:
                perimeter += 1
                edges.add(((x, y), (newx, newy)))


    # find edges
    edgecount = 0
    while len(edges) > 0:
        edgecount += 1
        q = [next(iter(edges))] 
        while len(q) > 0:
            a, b = q.pop()
            edges.remove((a, b))
            # horizontal
            if a[0] == b[0]:
                if (new := ((a[0]+1, a[1]), (b[0]+1, b[1]))) in edges:
                    q.append(new)
                if (new := ((a[0]-1, a[1]), (b[0]-1, b[1]))) in edges:
                    q.append(new)
            # vertical
            elif a[1] == b[1]:
                if (new := ((a[0], a[1]+1), (b[0], b[1]+1))) in edges:
                    q.append(new)
                if (new := ((a[0], a[1]-1), (b[0], b[1]-1))) in edges:
                    q.append(new)

    total += area * perimeter
    total2 += area * edgecount

print("Answer 1:", total)
print("Answer 2:", total2)
