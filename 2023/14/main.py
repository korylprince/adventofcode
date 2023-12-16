ROCK = "O"

def parse():
    G = set()
    rocks = set()
    with open("./input.txt") as f:
        for y, line in enumerate(f.read().strip().splitlines()):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    continue
                if char == ROCK:
                    rocks.add((x, y))
                    continue
                G.add((x, y))
    return G, rocks, x, y

def drop(G, rocks, x, y, dx, dy):
    G.add((x, y))
    rocks.remove((x, y))
    while (x + dx, y + dy) in G:
        x += dx
        y += dy
    G.remove((x, y))
    rocks.add((x, y))

dirs = ((0, -1), (-1, 0), (0, 1), (1, 0))

def drop_all(G, rocks, maxx, maxy, dx, dy):
    if dy == -1:
        order = ((x, y) for y in range(maxy+1) for x in range(maxx+1))
    elif dy == 1:
        order = ((x, y) for y in range(maxy, -1, -1) for x in range(maxx+1))
    elif dx == -1:
        order = ((x, y) for x in range(maxx+1) for y in range(maxy+1))
    elif dx == 1:
        order = ((x, y) for x in range(maxx, -1, -1) for y in range(maxy+1))
    for x, y in order:
        if (x, y) in rocks:
            drop(G, rocks, x, y, dx, dy)

def solve(rocks, maxy):
    return sum([maxy + 1 - y for _, y in rocks])
    
def part1():
    G, rocks, maxx, maxy = parse()
    drop_all(G, rocks, maxx, maxy, 0, -1)
    return solve(rocks, maxy)

print("Answer 1:", part1())

def run_cycle(G, rocks, maxx, maxy):
    for dx, dy in dirs:
        drop_all(G, rocks, maxx, maxy, dx, dy)

def find_pattern(matches):
    G, rocks, maxx, maxy = parse()
    patterns = dict()
    current = (0,) * (matches -1) + (solve(rocks, maxy),)
    for cycle in range(1_000_000_000):
        run_cycle(G, rocks, maxx, maxy)
        current = current[1:] + (solve(rocks, maxy),)
        if current in patterns:
            return patterns[current], cycle - patterns[current]
        patterns[current] = cycle
    
def part2():
    start, cycle = find_pattern(5)
    count = start + (1_000_000_000 - start) % cycle
    G, rocks, maxx, maxy = parse()
    for cycle in range(count):
        run_cycle(G, rocks, maxx, maxy)
    return solve(rocks, maxy)

print("Answer 2:", part2())
