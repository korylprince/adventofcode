with open("./input.txt") as f:
    grid = {(x, y): v for y, row in enumerate(f.read().strip().splitlines()) for x, v in enumerate(row.strip()) if v != "."}

bounds = (
    max([x for x, y in grid.keys()]),
    max([y for x, y in grid.keys()]),
)

def print_grid(grid, bounds):
    for y in range(bounds[1]+1):
        for x in range(bounds[0]+1):
            if (x, y) in grid:
                print(grid[(x, y)], end="")
            else:
                print(".", end="")
        print()

def move(grid, bounds):
    moves = []
    count = 0
    for x, y in [k for k, v in grid.items() if v == ">"]:
        if x < bounds[0] and (x+1, y) not in grid:
            moves.append(((x, y), (x+1, y)))
            count += 1
        elif x == bounds[0] and (0, y) not in grid:
            moves.append(((x, y), (0, y)))
            count += 1

    for old, new in moves:
        del grid[old]
        grid[new] = ">"

    moves.clear()

    for x, y in [k for k, v in grid.items() if v == "v"]:
        if y < bounds[1] and (x, y+1) not in grid:
            moves.append(((x, y), (x, y+1)))
            count += 1
        elif y == bounds[1] and (x, 0) not in grid:
            moves.append(((x, y), (x, 0)))
            count += 1

    for old, new in moves:
        del grid[old]
        grid[new] = "v"

    return count

count = None
iterations = 0
while count != 0:
    count = move(grid, bounds)
    iterations += 1

print("Answer 1:", iterations)
