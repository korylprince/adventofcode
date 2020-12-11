EMPTY = "L"
FLOOR = "."
OCCUPIED = "#"

grid = {}

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char == FLOOR:
                continue
            grid[(x, y)] = char

maxes = (max([x for x, y in grid.keys()]), max([y for x, y in grid.keys()]))

d = (
    (0, 1), (1, 1), (1, 0),
    (0, -1), (-1, -1), (-1, 0),
    (-1, 1), (1, -1),
)

def printGrid(grid):
    for y in range(maxes[1]+1):
        for x in range(maxes[0]+1):
            print(grid.get((x, y), FLOOR), end="")
        print("")

def round(grid):
    orig = grid.copy()
    changes = 0
    for (x, y), char in orig.items():
        occ = len([OCCUPIED for dx, dy in d if orig.get((x+dx, y+dy), "") == OCCUPIED])
        if char == EMPTY and occ == 0:
            grid[(x, y)] = OCCUPIED
            changes += 1
        elif char == OCCUPIED and occ >= 4:
            grid[(x, y)] = EMPTY
            changes += 1

    return changes

def round2(grid):
    orig = grid.copy()
    changes = 0
    for (x, y), char in orig.items():
        occ = 0
        for dx, dy in d:
            n = 1
            occn = 0
            while occn < 5 and 0 <= (x1 := x + dx*n) <= maxes[0] and 0 <= (y1 := y + dy*n) <= maxes[1]:
                if (c := orig.get((x1, y1), "")) == EMPTY:
                    break
                elif c == OCCUPIED:
                    occ += 1
                    occn += 1
                    break
                n += 1

        if char == EMPTY and occ == 0:
            grid[(x, y)] = OCCUPIED
            changes += 1
        elif char == OCCUPIED and occ >= 5:
            grid[(x, y)] = EMPTY
            changes += 1

    return changes

g = grid.copy()
while (changes := round(g)) != 0:
    pass
print("Answer 1:", list(g.values()).count(OCCUPIED))

g = grid.copy()
while (changes := round2(g)) != 0:
    pass
print("Answer 2:", list(g.values()).count(OCCUPIED))
