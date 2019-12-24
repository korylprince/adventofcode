BLOCK_BUG = "#"
BLOCK_EMPTY = "."


def str_grid(grid):
    s = []
    max_x = max([x for x, y in grid.keys()])
    max_y = max([y for x, y in grid.keys()])
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            s.append(grid[(x, y)])
        s.append("\n")
    return "".join(s)


def bio(grid):
    t = 0
    for i, c in enumerate(str_grid(grid).replace("\n", "")):
        if c == BLOCK_BUG:
            t += 2**i
    return t


def conway(grid):
    new = {}
    for (x, y), c in grid.items():
        count = 0
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if grid.get((x + d[0], y + d[1]), None) == BLOCK_BUG:
                count += 1
        if c == BLOCK_BUG:
            if count == 1:
                new[(x, y)] = BLOCK_BUG
            else:
                new[(x, y)] = BLOCK_EMPTY
        else:
            if 1 <= count <= 2:
                new[(x, y)] = BLOCK_BUG
            else:
                new[(x, y)] = BLOCK_EMPTY

    return new


grid = {}
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c

g = grid
seen = set(str_grid(g))
while (sg := str_grid(g := conway(g))) not in seen:
    seen.add(sg)

print("Answer:", bio(g))


def print_grid(grid):
    levels = sorted(set([l for x, y, l in grid.keys()]))
    for l in levels:
        print("Level", l)
        max_x = max([x for x, y, l in grid.keys()])
        max_y = max([y for x, y, l in grid.keys()])
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if x == 2 and y == 2:
                    print("?", end="")
                else:
                    print(grid[(x, y, l)], end="")
            print()


def conway2(grid):
    min_l = min([l for x, y, l in grid.keys()])
    max_l = max([l for x, y, l in grid.keys()])
    new = {(x, y, l): "." for x in range(5) for y in range(5) for l in range(min_l - 1, max_l + 2) if not(x == 2 and y == 2)}

    for x, y, l in new:
        count = 0
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            # check if center
            if (x + d[0], y + d[1]) == (2, 2):
                if x == 1:
                    count += sum([1 for y in range(5) if grid.get((0, y, l + 1), None) == BLOCK_BUG])
                if x == 3:
                    count += sum([1 for y in range(5) if grid.get((4, y, l + 1), None) == BLOCK_BUG])
                if y == 1:
                    count += sum([1 for x in range(5) if grid.get((x, 0, l + 1), None) == BLOCK_BUG])
                if y == 3:
                    count += sum([1 for x in range(5) if grid.get((x, 4, l + 1), None) == BLOCK_BUG])
            elif grid.get((x + d[0], y + d[1], l), None) == BLOCK_BUG:
                    count += 1

        # check if edge
        if x == 0 and grid.get((1, 2, l - 1), None) == BLOCK_BUG:
            count += 1
        if x == 4 and grid.get((3, 2, l - 1), None) == BLOCK_BUG:
            count += 1
        if y == 0 and grid.get((2, 1, l - 1), None) == BLOCK_BUG:
            count += 1
        if y == 4 and grid.get((2, 3, l - 1), None) == BLOCK_BUG:
            count += 1

        if grid.get((x, y, l), None) == BLOCK_BUG:
            if count == 1:
                new[(x, y, l)] = BLOCK_BUG
            else:
                new[(x, y, l)] = BLOCK_EMPTY
        else:
            if 1 <= count <= 2:
                new[(x, y, l)] = BLOCK_BUG
            else:
                new[(x, y, l)] = BLOCK_EMPTY

    return new


grid = {}
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(x, y, 0)] = c
    del grid[(2, 2, 0)]


g = grid
for _ in range(200):
    g = conway2(g)

print("Answer 2:", len([c for c in g.values() if c == BLOCK_BUG]))
