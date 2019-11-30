def check(grid, coord, goal, count):
    adj = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1))
    i = 0
    x, y = coord
    for dx, dy in adj:
        if x+dx < 0 or y+dy < 0:
            continue
        try:
            if grid[y+dy][x+dx] == goal:
                i += 1
                if i >= count:
                    return True
        except IndexError:
            continue
    return False


def step(grid):
    new = [[""] * len(row) for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == ".":
                if check(grid, (x, y), "|", 3):
                    new[y][x] = "|"
                else:
                    new[y][x] = "."
            elif grid[y][x] == "|":
                if check(grid, (x, y), "#", 3):
                    new[y][x] = "#"
                else:
                    new[y][x] = "|"
            elif grid[y][x] == "#":
                if check(grid, (x, y), "#", 1) and check(grid, (x, y), "|", 1):
                    new[y][x] = "#"
                else:
                    new[y][x] = "."

    return new


def print_grid(grid):
    for row in grid:
        print("".join(row))


def get_grid(file):
    with open(file) as f:
        return [list(line.strip()) for line in f.read().strip().splitlines()]


def score_grid(grid):
    wood = 0
    lumber = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid[y][x] == "|":
                wood += 1
            elif grid[y][x] == "#":
                lumber += 1

    return wood * lumber


def generate(grid, rounds):
    for i in range(rounds):
        grid = step(grid)

    return score_grid(grid)

def converge(grid, threshold=10):
    scores = set()
    root = None
    count = 0
    i = 1
    while True:
        grid = step(grid)
        score = score_grid(grid)
        if score in scores:
            if count == 0:
                root = (i, score)
            count += 1
            if count == threshold:
                break
        else:
            count = 0
            scores.add(score)
        i += 1

    i += 1
                
    while True:
        grid = step(grid)
        score = score_grid(grid)
        if score == root[1]:
            return root, i - root[0]
        i += 1


grid = get_grid("./input.txt")
print("Answer 1:", generate(grid, 10))

root, span = converge(grid)

print("Answer 2:", generate(grid, root[0] + ((1000000000 - root[0]) % span)))
