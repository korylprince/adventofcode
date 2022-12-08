G = dict()
with open("./input.txt") as f:
    for y, line in enumerate([line.strip() for line in f.read().strip().splitlines()]):
        for x, val in enumerate(line):
            G[(x, y)] = int(val)

len_x = len(set([x for x, _ in G.keys()]))
len_y = len(set([y for _, y in G.keys()]))

ring = (
    list(zip((-1,)*len_y, range(0, len_y))) +
    list(zip((len_x,)*len_y, range(0, len_y))) +
    list(zip(range(0, len_x), (-1,)*len_x)) +
    list(zip(range(0, len_x), (len_y,)*len_x))
)

seen = set()

for start in ring:
    x, y = start
    maximum = -1 
    dx, dy = [(dx, dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)) if (x+dx, y+dy) in G][0]
    while (x1 := x+dx, y1 := y+dy) in G:
        if (new := G[(x1, y1)]) > maximum:
            seen.add((x1, y1))
            maximum = new
        x, y = x1, y1

print("Answer 1:", len(seen))

scores = dict()

for start, t in G.items():
    score = 1
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        count = 0
        x, y = start
        while True:
            x1, y1 = x + dx, y + dy
            if (x1, y1) not in G:
                break
            if G[(x1, y1)] >= t:
                count += 1
                break
            if G[(x1, y1)] < t:
                count += 1
                x, y = x1, y1

        score *= count

    scores[start] = score

print("Answer 2:", max(scores.values()))
