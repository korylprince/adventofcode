from collections import defaultdict
G = defaultdict(lambda:-1)
TRAILHEAD = 0
TARGET = 9
trailheads = set()
d = ((1, 0), (-1, 0), (0, 1), (0, -1))

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            num = int(char) 
            G[(x, y)] = num
            if num == TRAILHEAD:
                trailheads.add((x, y))


def count(x, y):
    if G[(x, y)] == TARGET:
        return set(((x, y),))
    # recursively combine sets
    return set().union(*[count(x+dx, y+dy) for dx, dy in d if G[(x+dx, y+dy)] == G[(x, y)] + 1])

print("Answer 1:", sum([len(count(x, y)) for x, y in trailheads]))

def trails(parent):
    if G[parent[-1]] == TARGET:
        return set((parent,))

    x, y = parent[-1]
    return set().union(*[trails(parent + ((x+dx, y+dy),)) for dx, dy in d if G[(x+dx, y+dy)] == G[(x, y)] + 1])

print("Answer 2:", sum([len(trails(((x, y),))) for x, y in trailheads]))
